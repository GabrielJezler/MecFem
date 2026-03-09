import numpy as np

from ..wrapper import partializable
from ...displacement import Displacement

@partializable("mag")
def disp_1dof(X:np.ndarray, mag: float) -> np.ndarray:
    """
    Example displacement function.

    Parameters
    ----------
    X : ndarray
        Coordinates where the displacement is evaluated. This is an array of shape (n_dofs,).
    mag : float
        Magnitude of the displacement.

    Returns
    -------
    u : ndarray | float
        Displacement vector at the given coordinates. This is an array of shape (n_dofs,).

    """

    return mag * np.ones(X.shape[0])

class Displacement1Dof(Displacement):
    """
    Displacement function representing a linear displacement in one degree of freedom.

    Parameters
    ----------
    mag : float
        Magnitude of the displacement.
    """
    def __init__(self, mag: float) -> None:
        super().__init__(field=disp_1dof(mag=mag))
