import numpy as np

from MecFEM.utils import stress, kinematics, tensor

class LinearIsotropic:
    """
    This a base material class for isotropic materials. It defines the basic properties
    and methods that are common to all isotropic material models. To define a specific
    isotropic material model, you should inherit from this class and implement the 
    following methods: 
    
    - `stiffness`.
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
        if nu == 0.5 or nu == -1:
            raise ValueError("Poisson's ratio cannot be 0.5 or -1 for isotropic materials.")

        self._E = E
        self._nu = nu

        self._lambda = self._E * self._nu / ((1 + self._nu) * (1 - 2 * self._nu))
        self._mu = self._E / (2 * (1 + self._nu))

    def __repr__(self):
        return f"{self.__class__.__name__}(E={self.E}, nu={self.nu})"
    
    def __eq__(self, value):
        if isinstance(value, self.__class__):
            if self.E == value.E and self.nu == value.nu:
                return True

        return False

    @property
    def params(self):
        return f"E = {self.E}, nu = {self.nu}"

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
    
    def stiffness(self, dim: int):
        """
        Compute the stiffness tensor for the linear isotropic material.

        returns
        -------
        C : ndarray
            The stiffness tensor for the linear isotropic material. This is an array of shape (dim, dim, dim, dim).
        """
        raise NotImplementedError("This method should be implemented in the derived class.")
    
    def sigma(self, grad0_u):
        """
        Compute the Cauchy stress tensor for the linear isotropic material.

        Parameters
        ----------
        grad0_u : ndarray
            The gradient of the displacement field. This is an array of shape (n_int_pts, dim, dim).

        Returns
        -------
        sigma : ndarray
            The Cauchy stress tensor at integration points. This is an array of shape (n_int_pts, dim, dim).
        """
        eps = 1/2 * (grad0_u + tensor.transpose3(grad0_u))

        sigma = np.einsum('ijkl,nkl->nij', self.stiffness(dim=grad0_u.shape[1]), eps)

        return sigma
