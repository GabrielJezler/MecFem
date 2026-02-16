import numpy as np

from . import tensor
from .check import check_double_dimensions, check_single_dimension

def sigma2tau(sigma: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert Cauchy stress to Kirchhoff stress.
    
    Parameters
    ----------
    sigma : ndarray
        Cauchy stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F : ndarray
        Transformation gradient. This must match the shape of sigma.
        
    Returns
    -------
    tau : ndarray
        Kirchhoff stress tensor. This will have the same shape as sigma.
    
    """
    check_double_dimensions(sigma, F)
    J = np.linalg.det(F)
    if sigma.ndim == 2:
        tau = J * sigma
        return tau
    elif sigma.ndim == 3:
        tau = J[:, np.newaxis, np.newaxis] * sigma
        return tau

def sigma2pk1(sigma: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert Cauchy stress to First Piola-Kirchhoff stress.
    
    Parameters
    ----------
    sigma : ndarray
        Cauchy stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F : ndarray
        Transformation gradient. This must match the shape of sigma.

    Returns
    -------
    P : ndarray
        First Piola-Kirchhoff stress tensor. This will have the same shape as sigma.
    
    """
    check_double_dimensions(sigma, F)
    J = np.linalg.det(F)
    if sigma.ndim == 2:
        F_inv_T = np.linalg.inv(F).T
        P = J * sigma.dot(F_inv_T)
        return P
    elif sigma.ndim == 3:
        F_inv_T = tensor.transpose3(np.linalg.inv(F))
        P = J[:, np.newaxis, np.newaxis] * tensor.dot3(sigma, F_inv_T)
    return P

def sigma2pk2(sigma: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert Cauchy stress to Second Piola-Kirchhoff stress.
    
    Parameters
    ----------
    sigma : ndarray
        Cauchy stress tensor.This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F : ndarray
        Transformation gradient. This must match the shape of sigma.

    Returns
    -------
    S : ndarray
        Second Piola-Kirchhoff stress tensor. This will have the same shape as sigma.
    
    """
    check_double_dimensions(sigma, F)
    J = np.linalg.det(F)
    if sigma.ndim == 2:
        F_inv = np.linalg.inv(F)
        S = J * F_inv.dot(sigma).dot(F_inv.T)
        return S
    elif sigma.ndim == 3:
        F_inv = np.linalg.inv(F)
        S = J[:, np.newaxis, np.newaxis] * tensor.dot3(tensor.dot3(F_inv, sigma), tensor.transpose3(F_inv))
        return S

def tau2sigma(tau: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert Kirchhoff stress to Cauchy stress.
    
    Parameters
    ----------
    tau : ndarray
        Kirchhoff stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F : ndarray
        Transformation gradient. This must match the shape of tau.
        
    Returns
    -------
    sigma : ndarray
        Cauchy stress tensor. This will have the same shape as tau.
    """
    check_double_dimensions(tau, F)
    J = np.linalg.det(F)
    if tau.ndim == 2:
        sigma = tau / J
        return sigma
    elif tau.ndim == 3:
        sigma = tau / J[:, np.newaxis, np.newaxis]
        return sigma

def tau2pk1(tau: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert Kirchhoff stress to First Piola-Kirchhoff stress.
    
    Parameters
    ----------
    tau : ndarray
        Kirchhoff stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F
        Inverse transpose of Transformation gradient. This must match the shape of tau.
    
    Returns
    -------
    P : ndarray
        First Piola-Kirchhoff stress tensor. This will have the same shape as tau
    """
    check_double_dimensions(tau, F)
    if tau.ndim == 2:
        F_inv_T = np.linalg.inv(F).T
        P = tau.dot(F_inv_T)
        return P
    elif tau.ndim == 3:
        F_inv_T = tensor.transpose3(np.linalg.inv(F))
        P = tensor.dot3(tau, F_inv_T)
        return P

def tau2pk2(tau: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert Kirchhoff stress to Second Piola-Kirchhoff stress.
    
    Parameters
    ----------
    tau : ndarray
        Kirchhoff stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F
        Transformation gradient. This must match the shape of tau.

    Returns
    -------
    S : ndarray
        Second Piola-Kirchhoff stress tensor. This will have the same shape as tau.
    """
    check_double_dimensions(tau, F)
    if tau.ndim == 2:
        F_inv = np.linalg.inv(F)
        S = F_inv.dot(tau).dot(F_inv.T)
        return S
    elif tau.ndim == 3:
        F_inv = np.linalg.inv(F)
        S = tensor.dot3(tensor.dot3(F_inv, tau), tensor.transpose3(F_inv))
        return S

def pk12sigma(P: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert First Piola-Kirchhoff stress to Cauchy stress.
    
    Parameters
    ----------
    P : ndarray
        First Piola-Kirchhoff stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F
        Transformation gradient. This must match the shape of P.
    
    Returns
    -------
    sigma : ndarray
        Cauchy stress tensor. This will have the same shape as P.

    """
    check_double_dimensions(P, F)
    if P.ndim == 2:
        J = np.linalg.det(F)
        sigma = P.dot(F.T) / J
        return sigma
    elif P.ndim == 3:
        J = np.linalg.det(F)
        sigma = tensor.dot3(P, tensor.transpose3(F)) / J[:, np.newaxis, np.newaxis]
        return sigma

def pk12tau(P: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert First Piola-Kirchhoff stress to Kirchhoff stress.
    
    Parameters
    ----------
    P : ndarray
        First Piola-Kirchhoff stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F
        Transformation gradient. This must match the shape of P.

    Returns
    -------
    tau : ndarray
        Kirchhoff stress tensor. This will have the same shape as P.
    
    """
    check_double_dimensions(P, F)
    if P.ndim == 2:
        tau = P.dot(F.T)
        return tau
    elif P.ndim == 3:
        tau = tensor.dot3(P, tensor.transpose3(F))
        return tau

def pk12pk2(P: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert First Piola-Kirchhoff stress to Second Piola-Kirchhoff stress.
    
    Parameters
    ----------
    P : ndarray
        First Piola-Kirchhoff stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F
        Transformation gradient. This must match the shape of P.

    Returns
    -------
    S : ndarray
        Second Piola-Kirchhoff stress tensor. This will have the same shape as P.
    
    """
    check_double_dimensions(P, F)
    if P.ndim == 2:
        F_inv = np.linalg.inv(F)
        S = F_inv.dot(P)
        return S
    elif P.ndim == 3:
        F_inv = np.linalg.inv(F)
        S = tensor.dot3(F_inv, P)
        return S

def pk22sigma(S: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert Second Piola-Kirchhoff stress to Cauchy stress.
    
    Parameters
    ----------
    S : ndarray
        Second Piola-Kirchhoff stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F
        Transformation gradient. This must match the shape of S.

    Returns
    -------
    sigma : ndarray
        Cauchy stress tensor. This will have the same shape as S.
    
    """
    check_double_dimensions(S, F)
    if S.ndim == 2:
        J = np.linalg.det(F)
        sigma = (1 / J) * F.dot(S).dot(F.T)
        return sigma
    elif S.ndim == 3:
        J = np.linalg.det(F)
        sigma = (1 / J[:, np.newaxis, np.newaxis]) * tensor.dot3(tensor.dot3(F, S), tensor.transpose3(F))
        return sigma

def pk22tau(S: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert Second Piola-Kirchhoff stress to Kirchhoff stress.
    
    Parameters
    ----------
    S : ndarray
        Second Piola-Kirchhoff stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F
        Transformation gradient. This must match the shape of S.

    Returns
    -------
    tau : ndarray
        Kirchhoff stress tensor. This will have the same shape as S.
    
    """
    check_double_dimensions(S, F)
    if S.ndim == 2:
        tau = F.dot(S).dot(F.T)
        return tau
    elif S.ndim == 3:
        tau = tensor.dot3(tensor.dot3(F, S), tensor.transpose3(F))
        return tau

def pk22pk1(S: np.ndarray, F: np.ndarray) -> np.ndarray:
    """
    Convert Second Piola-Kirchhoff stress to First Piola-Kirchhoff stress.
    
    Parameters
    ----------
    S : ndarray
        Second Piola-Kirchhoff stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
    F
        Transformation gradient. This must match the shape of S.

    Returns
    -------
    P : ndarray
        First Piola-Kirchhoff stress tensor. This will have the same shape as S.
    
    """
    check_double_dimensions(S, F)
    if S.ndim == 2:
        P = F.dot(S)
        return P
    elif S.ndim == 3:
        P = tensor.dot3(F, S)
        return P

def von_mises(sigma: np.ndarray) -> float:
    """
    Compute von Mises stress from Cauchy stress tensor.
    
    Parameters
    ----------
    sigma : ndarray
        Cauchy stress tensor. This can be a 2nd or 3rd order tensor.
        The first indexfor the 3rd order tensor corresponds to different integration points if present.
        
    Returns
    -------
    sigma_vm : float
        von Mises stress. This will have the same shape as sigma.
        
    """
    check_single_dimension(sigma)
    if sigma.ndim == 2:
        s = sigma - np.trace(sigma) * np.eye(sigma.shape[0]) / 3
        sigma_vm = np.sqrt(3 * np.einsum('ij,ij->', s, s) / 2)
        return sigma_vm
    elif sigma.ndim == 3:
        s = sigma - tensor.trace3(sigma) * tensor.identity3(sigma.shape[1]) / 3  # Deviatoric stress
        sigma_vm = np.sqrt(3 * np.einsum('nij,nij->n', s, s) / 2)
        return sigma_vm
    
