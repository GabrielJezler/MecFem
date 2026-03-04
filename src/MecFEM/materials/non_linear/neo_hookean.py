import numpy as np

from ..base import NonLinearIsotropic
from ...utils import stress, kinematics, tensor

class NeoHookean(NonLinearIsotropic):
    """
    Defines the compressible Neo-Hookean material model.

    This considers the material to be defined by two parameters: Young's modulus E and
    Poisson's ratio nu. The material behavior is defined by the following law:

        S = μ * (I - C^(-1)) - λ * ln(J) * C^(-1)
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
        F = self.transformation_gradient(grad0_u)

        C = self.cauchy_green_right(F)
        C_inv = np.linalg.inv(C)

        J = np.linalg.det(F)

        S = self._mu * (tensor.identity3(C.shape[1]) - C_inv) + self._lambda * np.einsum('n, nij->nij', np.log(J), C_inv)
        return S

    def material_elastic(self, grad0_u):
        F = self.transformation_gradient(grad0_u)

        C = self.cauchy_green_right(F)
        C_inv = np.linalg.inv(C)

        J = np.linalg.det(F)

        dSdC = (1 / 2) * np.einsum('n, nNJgh->nNJgh', (self._mu - self._lambda * np.log(J)), (np.einsum('nNg, nJh->nNJgh', C_inv, C_inv) + np.einsum('nNh, nJg->nNJgh', C_inv, C_inv)))
        dSdC = dSdC + (1 /2) * self._lambda * np.einsum('ngh, nNJ->nNJgh', C_inv, C_inv)
   
        return 2 *dSdC
