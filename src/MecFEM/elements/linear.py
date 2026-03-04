import numpy as np

from .base import BaseFiniteElement

from ..geometry import isoparametric_elements as iso_elem
from ..mesh import Element
from ..utils import tensor, cache_none

class LinearFiniteElement(BaseFiniteElement):
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

    def update(self, material, *args, **kwargs) -> np.ndarray:
        """
        Update element state based on nodal displacements and material properties.

        Parameters
        ----------
        material : mf.materials
            Material model.

        Returns
        -------
        stiffness : ndarray
            Stiffness matrix of the element.

        """
        self.mat_stiffness = material.stiffness(self.dim)

        return self.mat_stiffness
    
    def simetric_gradient(self) -> np.ndarray:
        """
        Compute the symmetric gradient of the displacement field at integration points.

        Parameters
        ----------
        u_nodes : ndarray
            Nodal displacement field. This is an array of shape (n_nodes, dim).

        Returns
        -------
        B_sim : ndarray
            Symmetric gradient operator at integration points. This is an array of shape (n_int_pts, n_nodes, dim, dim, dim).
        """
        I2 = np.eye(self.dim)
        B_sim = 1/2 * (
            np.einsum('gak,lm->gamkl', self.dfshape(), I2) + 
            np.einsum('gal,km->gamkl', self.dfshape(), I2)
        )
        return B_sim

    def stiffness_matrix(self) -> np.ndarray:
        """
        Compute the stiffness matrix for the element.

        Returns
        -------
        stiffness : ndarray
            Stiffness matrix of the element. This is an array of shape (n_nodes, dim, n_nodes, dim).

        """
        stiffness = self.integrate(np.einsum('ijkl,gbmkl,gaj->gaibm', self.mat_stiffness, self.simetric_gradient(), self.dfshape()))
        return stiffness
    
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
        f_ext = self.integrate(np.einsum('ik,ij->ijk', f_int_pts, self.fshape()[:,:,0]))
        return f_ext

    def sigma(self, u_nodes, material) -> np.ndarray:
        """
        Compute the Cauchy stress tensor at integration points.

        Parameters
        ----------
        u_nodes : ndarray
            Nodal displacement field. This is an array of shape (n_nodes, dim).
        material : mf.materials
            Material model.

        Returns
        -------
        sigma : ndarray
            Cauchy stress tensor at integration points. This is an array of shape (n_int_pts, dim, dim).

        """
        grad0_u = self.gradient(u_nodes)
        sigma = material.sigma(grad0_u)

        return sigma
    
    def strain(self, u_nodes) -> np.ndarray:
        """
        Compute the strain tensor at integration points.

        Parameters
        ----------
        u_nodes : ndarray
            Nodal displacement field. This is an array of shape (n_nodes, dim).

        Returns
        -------
        epsilon : ndarray
            Strain tensor at integration points. This is an array of shape (n_int_pts, dim, dim).

        """
        grad0_u = self.gradient(u_nodes)
        epsilon = 0.5 * (grad0_u + np.transpose(grad0_u, (0, 2, 1)))

        return epsilon
