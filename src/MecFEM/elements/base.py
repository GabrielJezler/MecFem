import numpy as np

from ..geometry import isoparametric_elements as iso_elem
from ..mesh import Element
from ..utils import tensor, cache_none

class BaseFiniteElement:
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
        self.id = elem.id

        self.dim = elem_data.dim
        self.x_nodes = x_nodes

        self._int_pts = elem_data.integration_points
        self._shape = elem_data.shape_function

        self.weights = np.array(
            [elem_data.integration_points.W[i] for i in range(elem_data.integration_points.N)]
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(dim={self.dim}, n_nodes={self.n_nodes}, n_int_pts={self.n_int_pts})"

    @property
    def n_int_pts(self,):
        """ Get number of integration points per element """
        return self._int_pts.N

    @property
    def n_nodes(self,):
        """ Get number of nodes per element """
        return self.x_nodes.shape[0]

    @cache_none
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
            x = self._int_pts.X
        
        fshape = np.array(
            [self._shape.shape(x[i,:]) for i in range(x.shape[0])]
        )
        return fshape
    
    @cache_none
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
            x = self._int_pts.X
        
        dshape0 = np.array(
            [self._shape.dShape(x[i,:])[:, 0:self.dim] for i in range(x.shape[0])]
        )

        ##### HERE -> Add transpose #####
        # jacobian = np.array(
        #     [np.dot(dshape0[i, :, 0:self.dim].T, self.x_nodes[:, 0:self.dim]).T for i in range(x.shape[0])]
        # )
        jacobian = np.array(
            [np.einsum("ij, ik->jk", self.x_nodes[:, 0:self.dim], dshape0[i, :, 0:self.dim]) for i in range(x.shape[0])]
        )
        return jacobian
    
    @cache_none
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
            x = self._int_pts.X
        dshape0 = np.array(
            [self._shape.dShape(x[i,:])[:, 0:self.dim] for i in range(x.shape[0])]
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
        x_int_pts = np.einsum('ni,ik->nk', self.fshape(self._int_pts.X)[:,:,0], self.x_nodes)
        return x_int_pts
    
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
        
        jacobian_det = np.linalg.det(self.jacobian(self._int_pts.X))
        if tensor.ndim == 3:
            integral = np.einsum('i,ijk->jk', jacobian_det*self.weights, tensor)
        elif tensor.ndim == 5:
            integral = np.einsum('i,ijklm->jklm', jacobian_det*self.weights, tensor)
        else:
            raise ValueError(f"Tensor must be a 3D array with shape (n_int_pts, ..., ...) or 5D array with shape (n_int_pts, ..., ..., ..., ...), got {tensor.ndim}D array")

        return integral

    def apply_displacement(self, U: np.ndarray, t: float=0.0) -> np.ndarray:
        """
        Apply displacement boundary conditions to the nodal displacement field U.

        Parameters
        ----------
        U : ndarray
            Nodal displacement field. This is an array of shape (n_dofs).
        t : float
            Current time.

        Returns
        -------
        U_bc : ndarray
            Nodal displacement field with boundary conditions applied. This is an array of shape (n_dofs,).

        """
        U_bc = copy.deepcopy(U)
        nodes_coords = self.get_nodes_coordinates()

        for dofs, step in self._displacement_steps:
            U_bc[np.ix_(dofs)] = step.interp(t)(nodes_coords[dofs // self.dim, :])
        
        return U_bc


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
            x = self._int_pts.X

        grad0_u = np.einsum('inj,nk->ijk', self.dfshape(x), u_nodes)
        return grad0_u
