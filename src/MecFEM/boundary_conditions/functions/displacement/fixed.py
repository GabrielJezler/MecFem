import numpy as np

from ...displacement import Displacement

def fixed(X:np.ndarray) -> np.ndarray:
    """
    Fixed displacement function in one degree of freedom.

    Parameters
    ----------
    x : ndarray
        Coordinates where the displacement is evaluated. This is an array of shape (n_dofs,).

    Returns
    -------
    u : ndarray | float
        Displacement vector at the given coordinates. This is an array of shape (n_dofs,).

    """
    return np.zeros(X.shape[0])

class Fixed1Dof(Displacement):
    """
    Displacement function representing a fixed displacement in one degree of freedom.

    Parameters
    ----------
    None
    """
    def __init__(self) -> None:
        super().__init__(field=fixed)
