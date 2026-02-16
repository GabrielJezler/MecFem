import numpy as np

from . import tensor
from .check import check_single_dimension

""" Stress utilities """
def cauchy_green_right(F: np.ndarray) -> np.ndarray:
    """
    Compute the right Cauchy-Green deformation tensor.
    
    Parameters
    ----------
    F : ndarray
        Transformation gradient. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
        
    Returns
    -------
    C : ndarray
        Right Cauchy-Green deformation tensor. This will have the same shape as F.
    """
    check_single_dimension(F)
    if F.ndim == 2:
        C = F.T.dot(F)
        return C
    elif F.ndim == 3:
        C = tensor.dot3(tensor.transpose3(F), F)
        return C

def cauchy_green_left(F) -> np.ndarray:
    """
    Compute the left Cauchy-Green deformation tensor. 
    
    Parameters
    ----------
    F : ndarray
        Transformation gradient. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
        
    Returns
    -------
    b : ndarray
        Left Cauchy-Green deformation tensor. This will have the same shape as F.
    """
    check_single_dimension(F)
    if F.ndim == 2:
        b = F.dot(F.T)
        return b
    elif F.ndim == 3:
        b = tensor.dot3(F, tensor.transpose3(F))
        return b

def green_lagrange(F) -> np.ndarray:
    """
    Compute the Green-Lagrange strain tensor.
    
    Parameters
    ----------
    F : ndarray
        Transformation gradient. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
        
    Returns
    -------
    E : ndarray
        Green-Lagrange strain tensor. This will have the same shape as F.
    
    """
    check_single_dimension(F)
    C = cauchy_green_right(F)
    if F.ndim == 2:
        E = 0.5 * (C - np.eye(F.shape[0]))
        return E
    elif F.ndim == 3:
        E = 0.5 * (C - tensor.identity3(F.shape[1]))
        return E

def euler_almansi(F) -> np.ndarray:
    """
    Compute the Euler-Almansi strain tensor.
    
    Parameters
    ----------
    F : ndarray
        Transformation gradient. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
        
    Returns
    -------
    e : ndarray
        Euler-Almansi strain tensor. This will have the same shape as F.
    
    """
    check_single_dimension(F)
    b = cauchy_green_left(F)
    if F.ndim == 2:
        e = 0.5 * (np.eye(F.shape[0]) - np.linalg.inv(b))
        return e
    elif F.ndim == 3:
        e = 0.5 * (tensor.identity3(F.shape[1]) - tensor.inv3(b))
        return e


