import numpy as np

from ..base import NonLinearIsotropic
from ...utils import stress, kinematics, tensor

class StVenantKirchhoffElasticity(NonLinearIsotropic):
    """
    Defines the  St. Venant-Kirchhoff material model.

    This considers the material to be defined by two parameters: Young's modulus E and
    Poisson's ratio nu. The material behavior is defined by the following law:

        S = λ * tr(E) * I + 2μ * E
    """
    def __init__(self, E, nu):
        """
        Initialize the isotropic elastic material with Young's modulus and Poisson's 
        ratio.

        Parameters
        ----------
        E : float
            Young's modulus.
        nu : float
            Poisson's ratio.

        Returns
        -------
        None.

        """
        super().__init__(E, nu)        
    
    def sigma(self, grad0_u):
        """
        Compute the stress tensor given the displacement gradient tensor.

        Parameters
        ----------
        grad0_u : ndarray
            Displacement gradient tensor. This is an array of shape (n_int_pts, dim, dim).

        Returns
        -------
        sigma : ndarray
            Cauchy stress tensor. This is an array of shape (n_int_pts, dim, dim).

        """
        F = self.transformation_gradient(grad0_u)
        S = self.pk2(grad0_u)
        sigma = stress.pk22sigma(S, F)
        return sigma

    def tau(self, grad0_u):
        """
        Compute the Kirchhoff stress tensor given the displacement gradient tensor.

        Parameters
        ----------
        grad0_u : ndarray
            Displacement gradient tensor.

        Returns
        -------
        tau : ndarray
            Kirchhoff stress tensor.

        """
        pk2 = self.pk2(grad0_u)
        F = self.transformation_gradient(grad0_u)
        tau = stress.pk22tau(pk2, F)
        return tau
    
    def pk1(self, grad0_u):
        """
        Compute the First Piola-Kirchhoff stress tensor given the displacement gradient tensor.

        Parameters
        ----------
        grad0_u : ndarray
            Displacement gradient tensor.

        Returns
        -------
        P : ndarray
            First Piola-Kirchhoff stress tensor.

        """
        pk2 = self.pk2(grad0_u)
        F = self.transformation_gradient(grad0_u)
        P = stress.pk22pk1(pk2, F)
        return P
    
    def pk2(self, grad0_u):
        """
        Compute the Second Piola-Kirchhoff stress tensor given the displacement gradient tensor.

        Parameters
        ----------
        grad0_u : ndarray
            Displacement gradient tensor.

        Returns
        -------
        S : ndarray
            Second Piola-Kirchhoff stress tensor.

        """
        E = self.green_lagrange(self.transformation_gradient(grad0_u))
        S = self._lambda * tensor.trace3(E) * tensor.identity3(E.shape[1]) + 2 * self._mu * E
        return S

    def material_elastic_tangent(self, grad0_u):
        I3 = tensor.identity3(grad0_u.shape[1])
        return self._lambda * np.einsum('nNJ, ngh->nNJgh', I3, I3) + self._mu * (np.einsum('nNg, nJh->nNJgh', I3, I3) + np.einsum('nNh, nJg->nNJgh', I3, I3))

