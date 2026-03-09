import numpy as np

from ..wrapper import partializable
from ...volumetric import VolumetricForce

@partializable("g", "rho")
def gravity(X: np.ndarray, g: np.ndarray | float | int, rho: float) -> np.ndarray:
    """
    Constant electric field volumetric force function.

    Parameters
    ----------
    X : ndarray
        Coordinates where the force is evaluated. This is an array of shape (n_nodes, dim).
    g : np.ndarray | float | int
        Gravity field strength. If a np.ndarray, this has shape (dim,). If E is a
        scalar, then it will be converted to a vector with the same dimension as X,
        where all components are equal to g.
    rho : float
        Material density.

    Returns
    -------
    f : ndarray
        Volumetric force vector at the given coordinates. This is an array of shape (n_nodes, dim).
    """
    if isinstance(g, (int, float)):
        g = g * np.ones(X.shape[1])

    f = np.zeros_like(X)
    f[:, :] = g[np.newaxis, :] * rho
    return f

class Gravity(VolumetricForce):
    """
    Volumetric force representing a gravity field.

    Parameters
    ----------
    g : np.ndarray | float | int
        Gravity field strength. If a np.ndarray, this has shape (dim,). If E is a
        scalar, then it will be converted to a vector with the same dimension as X,
        where all components are equal to g.
    rho : float
        Material density.
    """
    def __init__(self, g: np.ndarray | float | int, rho: float) -> None:
        if not isinstance(g, np.ndarray):
            raise TypeError("g must be a numpy array")
        if g.ndim != 1:
            raise ValueError("g must be a 1D array")

        if isinstance(rho, (int, float)):
            rho = float(rho)
        if rho < 0:
            raise ValueError("rho must be non-negative")

        super().__init__(field=gravity(g=g, rho=rho))