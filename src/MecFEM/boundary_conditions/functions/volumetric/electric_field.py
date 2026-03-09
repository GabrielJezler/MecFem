import numpy as np

from ..wrapper import partializable
from ...volumetric import VolumetricForce

@partializable("E", "rho_e")
def constant_electric_field(X: np.ndarray, E: np.ndarray, rho_e: float) -> np.ndarray:
    """
    Constant electric field volumetric force function.

    Parameters
    ----------
    X : ndarray
        Coordinates where the force is evaluated. This is an array of shape (n_nodes, dim).
    E : np.ndarray
        Electric field strength. If a np.ndarray, this has shape (dim,).
    rho_e : float
        Electric charge density.

    Returns
    -------
    f : ndarray
        Volumetric force vector at the given coordinates. This is an array of shape (n_nodes, dim).
    """
    f = np.zeros_like(X)
    f[:, :] = E[np.newaxis, :] * rho_e
    return f

class ConstantElectricField(VolumetricForce):
    """
    Volumetric force representing a spatially constant electric field.

    Parameters
    ----------
    E : np.ndarray
        Electric field strength. If a np.ndarray, this has shape (dim,).
    rho_e : float
        Electric charge density.
    """
    def __init__(self, E: np.ndarray, rho_e: float) -> None:
        if not isinstance(E, np.ndarray):
            raise TypeError("E must be a numpy array")
        if E.ndim != 1:
            raise ValueError("E must be a 1D array")

        if isinstance(rho_e, (int, float)):
            rho_e = float(rho_e)
        if rho_e < 0:
            raise ValueError("rho_e must be non-negative")

        super().__init__(field=constant_electric_field(E=E, rho_e=rho_e))