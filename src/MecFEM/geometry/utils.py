import numpy as np
import scipy.special as sp

# def gll_nodes(n):
#     """Compute the Gauss-Lobatto-Legendre (GLL) points for a polynomial of order n."""
#     P = sp.legendre(n)
#     dP = P.deriv()
#     interior_nodes = np.roots(dP)
#     gll_nodes = np.concatenate(([-1, 1], np.sort(interior_nodes)))

#     return gll_nodes

def lagrange_nodes(n):
    """Compute the Lagrange points for a polynomial of order n."""
    lagrange_nodes = np.linspace(-1, 1, n+1)
    lagrange_nodes = np.concatenate((lagrange_nodes[[0, -1]], lagrange_nodes[1:-1]))

    return lagrange_nodes
