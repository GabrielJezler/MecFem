import numpy as np

def dot3(A, B):
    """
    Perform the multiplicatifon of the firts and second axis 
    between two 3rd order tensors A and B.

    Parameters
    ----------
    A : ndarray
        First 3rd order tensor. Shape: (n, i, k)
    B : ndarray
        Second 3rd order tensor. Shape: (n, k, j)

    Returns
    -------
    C : ndarray
        Resulting 3rd order tensor after dot product. Shape: (n, i, j)

    """
    return np.einsum('nik,nkj->nij', A, B)

def trace3(A):
    """
    Compute the trace of a 3rd order tensor A considering the first
    and second axes.

    Parameters
    ----------
    A : ndarray
        Input 3rd order tensor. Shape: (n, i, i)

    Returns
    -------
    tr : ndarray
        Trace of the tensor for each slice. Shape: (n, 1, 1)

    """
    return np.trace(A, axis1=1, axis2=2)[:, np.newaxis, np.newaxis]

def transpose3(A):
    """
    Transpose the last two axes of a 3rd order tensor A.

    Parameters
    ----------
    A : ndarray
        Input 3rd order tensor. Shape: (n, i, j)

    Returns
    -------
    A_T : ndarray
        Transposed 3rd order tensor. Shape: (n, j, i)

    """
    return np.transpose(A, axes=(0,2,1))

def identity3(dim):
    """
    Create a 3rd order identity tensor of given dimension.

    Parameters
    ----------
    dim : int
        Dimension of the identity tensor.

    Returns
    -------
    I : ndarray
        3rd order identity tensor. Shape: (1, dim, dim)

    """
    return np.eye(dim)[np.newaxis, :, :]

