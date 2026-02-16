import numpy as np

def check_double_dimensions(A: np.ndarray, B: np.ndarray):
    """
    Check if the dimensions of A and A gradient tensors are compatible.

    Parameters
    ----------
    A : ndarray
        Tensor A. This can be a 2nd or 3rd order tensor.
    B : ndarray
        Tensor B. This must match the shape of A.

    Raises
    ------
    ValueError
        If the dimensions of A and B tensors are not compatible.
        
    """
    if not(A.ndim == 2 or A.ndim == 3):
        raise ValueError("Input A must be a 2nd or 3rd order tensor.")
    elif A.shape != B.shape:
        raise ValueError("Incompatible dimensions between tensors A and B.")
    
def check_single_dimension(A: np.ndarray):
    """
    Check if the input A is a 2nd or 3rd order tensor.

    Parameters
    ----------
    A : ndarray
        Input tensor. This can be a 2nd or 3rd order tensor.

    Raises
    ------
    ValueError
        If the input tensor is not a single 2nd order tensor.
        
    """
    if not(A.ndim == 2 or A.ndim == 3):
        raise ValueError("Input A must be a single 2nd order tensor.")