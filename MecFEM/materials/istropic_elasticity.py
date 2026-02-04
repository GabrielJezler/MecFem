import numpy as np

from MecFEM.utils import stress, kinematics, tensor

class IsotropicElasticity:
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
        self._E = E
        self._nu = nu

        self._lambda = self._E * self._nu / ((1 + self._nu) * (1 - 2 * self._nu))
        self._mu = self._E / (2 * (1 + self._nu))

    @property
    def E(self):
        """Young's modulus"""
        return self._E
    
    @property
    def nu(self):
        """Poisson's ratio"""
        return self._nu
    
    @property
    def lame1(self):
        """Lame's first parameter (lambda)"""
        return self._lambda
    
    @property
    def lame2(self):
        """Lame's second parameter (mu)"""
        return self._mu

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
    
    def transformation_gradient(self, grad0_u):
        """
        Compute the transformation gradient tensor.

        Parameters
        ----------
        grad0_u : ndarray
            Displacement gradient tensor. This is an array of shape (n_int_pts, dim, dim).

        Returns
        -------
        F : ndarray
            Transformation gradient tensor. This is an array of shape (n_int_pts, dim, dim).

        """
        F = grad0_u + tensor.identity3(grad0_u.shape[1])
        return F

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

    def cauchy_green_right(self, F):
        """
        Compute the right Cauchy-Green deformation tensor.
        
        Parameters
        ----------
        F : ndarray
            Deformation gradient.
            
        Returns
        -------
        C : ndarray
            Right Cauchy-Green deformation tensor.
        """
        return kinematics.cauchy_green_right(F)
    
    def cauchy_green_left(self, F):
        """
        Compute the left Cauchy-Green deformation tensor.
        
        Parameters
        ----------
        F : ndarray
            Deformation gradient.
            
        Returns
        -------
        b : ndarray
            Left Cauchy-Green deformation tensor.
        """
        return kinematics.cauchy_green_left(F)
    
    def green_lagrange(self, F):
        """
        Compute the Green-Lagrange strain tensor.
        
        Parameters
        ----------
        F : ndarray
            Deformation gradient.
            
        Returns
        -------
        E : ndarray
            Green-Lagrange strain tensor.
        """
        return kinematics.green_lagrange(F)
    
    def euler_almansi(self, F):
        """
        Compute the Euler-Almansi strain tensor.
        
        Parameters
        ----------
        F : ndarray
            Deformation gradient.
            
        Returns
        -------
        eA : ndarray
            Euler-Almansi strain tensor.
        """
        return kinematics.euler_almansi(F)
    


