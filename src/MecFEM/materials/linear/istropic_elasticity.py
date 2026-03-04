import numpy as np

from ..base import LinearIsotropic

class IsotropicElasticity(LinearIsotropic):
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

    def stiffness(self, dim: int):
        """
        Compute the stiffness tensor for the linear isotropic material.
        """
        I2 = np.eye(dim)
        return self._lambda * np.einsum('ij,kl->ijkl', I2, I2) + self._mu * (np.einsum('ik,jl->ijkl', I2, I2) + np.einsum('il,jk->ijkl', I2, I2))

