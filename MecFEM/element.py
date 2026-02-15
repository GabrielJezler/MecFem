import numpy as np

from .geometry import isoparametric_elements as iso_elem
from .mesh import Element
from .utils import tensor

class NonLinearFiniteElement:
    """
    Basic data structure for finite element

    Attributes
    ----------
    x_nodes : ndarray
        Coordinates of the element nodes. Indexing: x_nodes[n_nodes, dim]
    fshape : ndarray
        Shape functions evaluated at integration points. Indexing: fshape[n_int_pts, n_nodes, 1]
    jacobian : ndarray
        Jacobian matrices at integration points. Indexing: jacobian[n_int_pts, dim, dim]
    dfshape : ndarray
        Derivatives of shape functions with respect to global coordinates at integration points. Indexing: dfshape[n_int_pts, n_nodes, dim]
    weight : ndarray
        Weights for each integration point. Indexing: weight[n_int_pts]
    """
    def __init__(self, elem: Element, x_nodes: np.ndarray) -> None:
        elem_data: iso_elem.ReferenceElementData = iso_elem.ReferenceElements().get_by_type(elem.type)

        self.dim = elem_data.dim
        self.x_nodes = x_nodes

        self.__int_pts = elem_data.integration_points
        self.__shape = elem_data.shape_function

        self.weights = np.array(
            [elem_data.integration_points.W[i] for i in range(elem_data.integration_points.N)]
        )

    @property
    def n_int_pts(self,):
        """ Get number of integration points per element """
        return self.__int_pts.N

    @property
    def n_nodes(self,):
        """ Get number of nodes per element """
        return self.x_nodes.shape[0]

    def fshape(self, x: np.ndarray | None = None) -> np.ndarray:
        """
        Compute the shape functions at given local coordinates.

        Parameters
        ----------
        x : ndarray
            Local coordinates where to evaluate the shape functions. This is an array of shape (N, dim).

        Returns
        -------
        fshape : ndarray
            Shape functions evaluated at the given local coordinates. This is an array of shape (N, n_nodes, 1).    
        """
        if x is None:
            x = self.__int_pts.X
        
        fshape = np.array(
            [self.__shape.shape(x[i,:]) for i in range(x.shape[0])]
        )
        return fshape
    
    def jacobian(self, x: np.ndarray | None = None) -> np.ndarray:
        """
        Compute the Jacobian matrices at given local coordinates.

        Parameters
        ----------
        x : ndarray
            Local coordinates where to evaluate the Jacobian. This is an array of shape (N, dim).

        Returns
        -------
        jacobian : ndarray
            Jacobian matrices at the given local coordinates. This is an array of shape (N, dim, dim).    
        """
        if x is None:
            x = self.__int_pts.X
        
        dshape0 = np.array(
            [self.__shape.dShape(x[i,:])[:, 0:self.dim] for i in range(x.shape[0])]
        )

        ##### HERE -> Add transpose #####
        # jacobian = np.array(
        #     [np.dot(dshape0[i, :, 0:self.dim].T, self.x_nodes[:, 0:self.dim]).T for i in range(x.shape[0])]
        # )
        jacobian = np.array(
            [np.einsum("ij, ik->jk", self.x_nodes[:, 0:self.dim], dshape0[i, :, 0:self.dim]) for i in range(x.shape[0])]
        )
        return jacobian
    
    def dfshape(self, x: np.ndarray | None = None) -> np.ndarray:
        """
        Compute the derivatives of the shape functions with respect to global coordinates at given local coordinates.

        Parameters
        ----------
        x : ndarray
            Local coordinates where to evaluate the derivatives of the shape functions. This is an array of shape (N, dim).

        Returns
        -------
        dfshape : ndarray
            Derivatives of the shape functions with respect to global coordinates at the given local coordinates. This is an array of shape (N, n_nodes, dim).    
        """
        if x is None:
            x = self.__int_pts.X
        dshape0 = np.array(
            [self.__shape.dShape(x[i,:])[:, 0:self.dim] for i in range(x.shape[0])]
        )

        jacobian = self.jacobian(x)

        dfshape = np.array(
            [np.dot(dshape0[i, : , :], np.linalg.inv(jacobian[i, :, :])) for i in range(x.shape[0])]
        )
        return dfshape

    def x_int_pts(self) -> np.ndarray:
        """
        Compute the coordinates of the integration points.

        Returns
        -------
        x_int_pts : ndarray
            Coordinates of the integration points. This is an array of shape (n_int_pts, dim).

        """
        x_int_pts = np.einsum('ni,ik->nk', self.fshape(self.__int_pts.X)[:,:,0], self.x_nodes)
        return x_int_pts

    def gradient(self, u_nodes, x: np.ndarray | None = None) -> np.ndarray:
        """
        Compute the gradient of a field u at integration points.

        Parameters
        ----------
        u_nodes : ndarray
            Nodal values of the field. This is an array of shape (n_nodes, dim).

        Returns
        -------
        grad_u : ndarray
            Gradient of the field at integration points. This is an array of shape (n_int_pts, dim, dim).
        
        """
        if x is None:
            x = self.__int_pts.X
        grad0_u = np.einsum('inj,nk->ijk', self.dfshape(x), u_nodes)
        return grad0_u

    def update(self, u_nodes, material):
        """
        Update element state based on nodal displacements and material properties.

        Parameters
        ----------
        u_nodes : ndarray
            Nodal displacement field. This is an array of shape (n_nodes, dim).
        material : mf.materials
            Material model.

        Returns
        -------
        pk1 : ndarray
            First Piola-Kirchhoff stress tensor at integration points.

        """
        self.grad0_u = self.gradient(u_nodes)

        self.pk1 = material.pk1(self.grad0_u)
        self.stiffness = material.stiffness(self.grad0_u)

        return self.stiffness, self.pk1, self.grad0_u
    
    def integrate(self, tensor:np.ndarray) -> np.ndarray:
        """
        Integrate a tensor field over the element using numerical integration.

        Parameters
        ----------
        tensor : ndarray
            Tensor field at integration points. This is an array of shape (n_int_pts, ...).

        Returns
        -------
        integral : ndarray
            Integrated tensor over the element.

        """
        if tensor.shape[0] != self.n_int_pts:
            raise ValueError(f"Tensor first dimension must match number of integration points: expected {self.n_int_pts}, got {tensor.shape[0]}")
        
        jacobian_det = np.linalg.det(self.jacobian(self.__int_pts.X))
        if tensor.ndim == 3:
            integral = np.einsum('i,ijk->jk', jacobian_det*self.weights, tensor)
        elif tensor.ndim == 5:
            integral = np.einsum('i,ijklm->jklm', jacobian_det*self.weights, tensor)
        else:
            raise ValueError(f"Tensor must be a 3D array with shape (n_int_pts, ..., ...) or 5D array with shape (n_int_pts, ..., ..., ..., ...), got {tensor.ndim}D array")

        return integral

    def internal_force(self) -> np.ndarray:
        """
        Compute the internal force vector for the element.

        Returns
        -------
        fint : ndarray
            Internal force vector. This is an array of shape (n_nodes, dim).

        """
        # fint = np.einsum('i,ijk->jk', self.jacobian_det*self.weight, tensor.dot3(self.dfshape, self.pk1))
        fint = self.integrate(tensor.dot3(self.dfshape(), self.pk1))
        return fint
    
    def volumetric_force(self, f_int_pts) -> np.ndarray:
        """
        Compute the volumetric force vector for the element.

        Parameters
        ----------
        f_int_pts : ndarray
            Body force vector at integration points. This is an array of shape (n_int_pts, dim).

        Returns
        -------
        fvol : ndarray
            Volumetric force vector. This is an array of shape (n_nodes, dim).

        """
        # f_vol = np.einsum('i,ik,ij->jk', self.jacobian_det*self.weight, f_int_pts, self.fshape[:,:,0])
        f_vol = self.integrate(np.einsum('ik,ij->ijk', f_int_pts, self.fshape()[:,:,0]))
        return f_vol
    
    def external_force(self, f_int_pts) -> np.ndarray:
        """
        Compute the external force vector for the element.

        Parameters
        ----------
        f_int_pts : ndarray
            Traction vector at the integration points. This is an array of shape (n_int_pts, dim).

        Returns
        -------
        f_ext : ndarray
            External force vector. This is an array of shape (n_nodes, dim).

        """
        # f_ext = np.einsum('i,ik,ij->jk', self.jacobian_det*self.weight, f_int_pts, self.fshape[:,:,0])
        f_ext = self.integrate(np.einsum('ik,ij->ijk', f_int_pts, self.fshape()[:,:,0]))
        return f_ext
    
    def stiffness_matrix(self):
        """
        compute internal stiffness of the element

        Returns
        -------
        K : 4-entry tensor
            internal stiffness of the element.
        """
        Kint = self.integrate(np.einsum('naJ,niJkL,nbL->naibk', self.dfshape(), self.stiffness, self.dfshape()))

        K = Kint
        return K
    
    def sigma(self, u_nodes, material) -> np.ndarray:
        """
        Compute the Cauchy stress tensor at integration points.

        Returns
        -------
        sigma : ndarray
            Cauchy stress tensor at integration points. This is an array of shape (n_int_pts, dim, dim).

        """
        grad0_u = self.gradient(u_nodes)
        sigma = material.sigma(grad0_u)

        return sigma
