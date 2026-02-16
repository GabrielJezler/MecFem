import numpy as np

from ...utils import stress, kinematics, tensor
from ..base import Isotropic

class IsotropicElasticity(Isotropic):
    """
    Defines an isotropic linear elastic material model.

    This considers the material to be defined by two parameters: Young's modulus E and Poisson's ratio nu.
    The material behavior is defined by Hooke's law for isotropic materials:

        σ = λ * tr(ε) * I + 2μ * ε
    """
    def __init__(self, E, nu):
        """
        Initialize the isotropic elastic material with Young's modulus and Poisson's ratio.

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

    def epsilon(self, grad0_u):
        """
        Compute the stress tensor given the strain tensor using Hooke's law.

        Parameters
        ----------
        grad0_u : ndarray
            Displacement gradient tensor. This is an array of shape (n_int_pts, dim, dim).

        Returns
        -------
        epsilon : ndarray
            Strain tensor. This is an array of shape (n_int_pts, dim, dim).

        """
        epsilon = 0.5 * (grad0_u + tensor.transpose3(grad0_u))
        return epsilon
    
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
        epsilon = self.epsilon(grad0_u)

        sigma = self._lambda * tensor.trace3(epsilon) * tensor.identity3(epsilon.shape[1]) + 2 * self._mu * epsilon
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
        sigma = self.sigma(grad0_u)
        F = self.transformation_gradient(grad0_u)
        tau = stress.sigma2tau(sigma, F)
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
        sigma = self.sigma(grad0_u)
        F = self.transformation_gradient(grad0_u)
        P = stress.sigma2pk1(sigma, F=F)
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
        sigma = self.sigma(grad0_u)
        F = self.transformation_gradient(grad0_u)
        S = stress.sigma2pk2(sigma, F=F)
        return S
