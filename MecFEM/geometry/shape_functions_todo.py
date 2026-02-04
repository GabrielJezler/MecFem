import numpy as np
from .utils import lagrange_nodes

""" --- Shape functions 0D --- """
class LagrangePoint:
    """Shape functions for 0D point element"""
    def __init__(self, nodes:np.ndarray):
        """Initialize with given nodes"""
        self.nodes = nodes
        self.order = 1

    @staticmethod
    def shape(x):
        """Returns shape functions"""
        return np.array([[1.0]])

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        return np.array([[0.0]])


""" --- Shape functions 1D --- """
class LagrangeLine:
    """Shape functions for 1D Lagrange elements"""
    def __init__(self, nodes):
        """Initialize with given nodes"""
        self.nodes = nodes
        self.order = nodes.shape[0] - 1
        
    def basis(self, x, check):
        """
        Returns the basis check[0] at x
        The first element of check is the index for the basis
        """
        return np.prod(
            [(x - self.nodes[j]) / (self.nodes[check[0]] - self.nodes[j]) for j in range(self.nodes.shape[0]) if j not in check]
        )

    def shape(self, x):
        """Returns shape functions"""
        N = np.array([self.basis(x, [i]) for i in range(self.nodes.shape[0])])
        return N[np.newaxis].T

    def dShape(self, x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        dN = np.array(
            [
                np.sum(
                    [
                        1/(self.nodes[i]-self.nodes[j])*self.basis(x, [i, j]) for j in range(self.nodes.shape[0]) if j !=i
                    ] 
                ) for i in range(self.nodes.shape[0])
            ] 
        )
        return dN[np.newaxis].T


""" --- Shape functions 2D --- """
class LagrangeQuad:
    """Shape functions for 2D Lagrange elements"""
    def __init__(self, nodes):
        """Initialize with given polynomial order"""
        self.nodes = nodes
        self.order = int(np.sqrt(nodes.shape[0]) - 1)

    def basis(self, x:np.ndarray, check:list[int]) -> float:
        """
        Returns the basis check[0] at x
        The first element of check is the index for the basis
        """
        base_nodes = np.linspace(-1, 1, self.order + 1)
        return np.prod(
            [(x - base_nodes[j]) / (base_nodes[check[0]] - base_nodes[j]) for j in range(self.order + 1) if j not in check]
        )

    def shape(self, x):
        """Returns shape functions"""
        N_xi = np.array([self.basis(x[0], [i]) for i in range(self.order + 1)])
        N_eta = np.array([self.basis(x[1], [i]) for i in range(self.order + 1)])

        N = np.array([N_xi[i]*N_eta[j] for j in range(self.order + 1) for i in range(self.order + 1)])
        return N[np.newaxis].T

    def dShape(self, x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        dN = np.array(
            [
                np.sum(
                    [
                        1/(self.nodes[i]-self.nodes[j])*self.basis(x, [i, j]) for j in range(self.order+1) if j !=i
                    ] 
                ) for i in range(self.order+1)
            ] 
        )
        return dN[np.newaxis].T
    
class LagrangeQuad8():
    """Shape functions for 2D Lagrange Serendipity elements"""
    def __init__(self, nodes:np.ndarray):
        """Initialize with given polynomial order"""
        pass
