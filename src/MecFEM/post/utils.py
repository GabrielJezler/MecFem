import numpy as np 

def interpolate_time(U: np.ndarray, time: np.ndarray, t: float) -> np.ndarray:
    """
    Interpolate the displacement field U at time t.

    Parameters
    ----------
    U : ndarray
        Displacement field at different time steps. This is an array of shape (n_time_steps, n_dofs).
    
    time : ndarray
        Time steps corresponding to the displacement field U. This is an array of shape (n_time_steps,).

    t : float
        The time at which to interpolate the displacement field.

    Returns
    -------
    u : ndarray
        Interpolated displacement field at time t. This is an array of shape (n_dofs,).
    """
    # Handle edge cases
    if t <= time[0]:
        return U[0]
    if t >= time[-1]:
        return U[-1]
    
    # Find the indices of the two time steps that bracket t
    idx = np.searchsorted(time, t)
    
    # Linear interpolation
    t0, t1 = time[idx - 1], time[idx]
    U0, U1 = U[idx - 1], U[idx]
    
    # Interpolation factor
    alpha = (t - t0) / (t1 - t0)
    
    # Interpolate
    u = U0 + alpha * (U1 - U0)
    
    return u
    