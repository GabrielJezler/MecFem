import numpy as np

from .base import BaseFiniteElement

from ..mesh import Element
from ..utils import tensor

class NonLinearFiniteElement(BaseFiniteElement):
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
        super().__init__(elem, x_nodes)

    def update(self, material, u_nodes: np.ndarray, *args, **kwargs) -> np.ndarray:
        """
        Update element state based on nodal displacements and material properties.

        Parameters
        ----------
        material : mf.materials
            Material model.
        u_nodes : ndarray
            Nodal displacement field. This is an array of shape (n_nodes, dim).

        Returns
        -------
        pk1 : ndarray
            First Piola-Kirchhoff stress tensor at integration points.

        """
        self.grad0_u = self.gradient(u_nodes)

        self.pk1 = material.pk1(self.grad0_u)
        self.mixed_elastic_tangent = material.mixed_elastic_tangent(self.grad0_u)

        return self.mixed_elastic_tangent, self.pk1, self.grad0_u

    def internal_force(self) -> np.ndarray:
        """
        Compute the internal force vector for the element.

        Returns
        -------
        fint : ndarray
            Internal force vector. This is an array of shape (n_nodes, dim).

        """
        fint = self.integrate(tensor.dot3(self.dfshape(), self.pk1))
        return fint
    
    def volumetric_force(self, f_int_pts: np.ndarray) -> np.ndarray:
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
        f_vol = self.integrate(np.einsum('ik,ij->ijk', f_int_pts, self.fshape()[:,:,0]))
        return f_vol
    
    def external_force(self, f_int_pts: np.ndarray) -> np.ndarray:
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
        f_ext = self.integrate(np.einsum('ik,ij->ijk', f_int_pts, self.fshape()[:,:,0]))
        return f_ext
    
    def internal_tangent_matrix(self) -> np.ndarray:
        """
        compute internal tangent matrix of the element

        Returns
        -------
        Kint : 4-entry tensor
            internal tangent matrix of the element. This is an array of shape (n_nodes, dim, n_nodes, dim).
        """
        Kint = self.integrate(np.einsum('naJ,niJkL,nbL->naibk', self.dfshape(), self.mixed_elastic_tangent, self.dfshape()))

        return Kint
