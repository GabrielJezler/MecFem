import numpy as np

from MecFEM.utils import stress, kinematics, tensor

class StVenantKirchhoffElasticity:
    """
    
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

    def material_elastic(self, grad0_u):
        I3 = tensor.identity3(grad0_u.shape[1])
        return self._lambda * np.einsum('nNJ, ngh->nNJgh', I3, I3) + self._mu * (np.einsum('nNg, nJh->nNJgh', I3, I3) + np.einsum('nNh, nJg->nNJgh', I3, I3))

    def stiffness(self, grad0_u):
        F = self.transformation_gradient(grad0_u)
        I2 = np.eye(F.shape[1])

        dEdF = 1/2 * (np.einsum('gL,nkh->nghkL', I2, F) + np.einsum('hL,nkg->nghkL', I2, F))

        t1 = np.einsum('ik,nJL->niJkL', I2, self.pk2(grad0_u))
        t2 = np.einsum('niN, nNJgh, nghkL->niJkL', F, self.material_elastic(grad0_u), dEdF)

        return t1 + t2

