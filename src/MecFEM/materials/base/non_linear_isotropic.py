import numpy as np

from .linear_isotropic import LinearIsotropic

from ...utils import kinematics, tensor
from ...utils import classification as cl

class NonLinearIsotropic(LinearIsotropic):
    """
    This a base material class for isotropic materials. It defines the basic properties
    and methods that are common to all isotropic material models. To define a specific
    isotropic material model, you should inherit from this class and implement the 
    necessary methods.
    """
    def __init__(self, E, nu):
        super().__init__(E, nu)

        self._behavior = cl.MaterialBehavior.ELASTIC
        self._symmetry = cl.MaterialSymmetry.ISOTROPIC
        self._solver = cl.SolverClassification.NON_LINEAR

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
        raise NotImplementedError("This method should be implemented in the derived class.")

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
        raise NotImplementedError("This method should be implemented in the derived class.")
    
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
        raise NotImplementedError("This method should be implemented in the derived class.")

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
        raise NotImplementedError("This method should be implemented in the derived class.")

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

    def material_elastic_tangent(self, grad0_u):
        """
        Compute the material elastic tangent tensor.

        Parameters
        ----------
        grad0_u : ndarray
            Displacement gradient tensor. This is an array of shape (n_int_pts, dim, dim).

        Returns
        -------
        dS/dE : ndarray
            Material elastic tangent tensor. This is an array of shape (n_int_pts, dim, dim, dim, dim).
        """
        raise NotImplementedError("This method should be implemented in the derived class.")

    def mixed_elastic_tangent(self, grad0_u):
        """
        Compute the mixed elastic tangent tensor.

        Parameters
        ----------
        grad0_u : ndarray
            Displacement gradient tensor. This is an array of shape (n_int_pts, dim, dim).

        Returns
        -------
        dP/dF : ndarray
            Mixed elastic tangent tensor. This is an array of shape (n_int_pts, dim, dim, dim, dim).
        """
        F = self.transformation_gradient(grad0_u)
        I2 = np.eye(F.shape[1])

        dEdF = 1/2 * (np.einsum('gL,nkh->nghkL', I2, F) + np.einsum('hL,nkg->nghkL', I2, F))

        t1 = np.einsum('ik,nJL->niJkL', I2, self.pk2(grad0_u))
        t2 = np.einsum('niN, nNJgh, nghkL->niJkL', F, self.material_elastic_tangent(grad0_u), dEdF)

        return t1 + t2

