import numpy as np
from .utils import lagrange_nodes

""" --- Shape functions 0D --- """
class LagrangePoint:
    """
    Shape functions for: 
        dim: 0 
        formulation: Lagrange
        element: Point
        n_nodes: 1
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        return np.array([[1.0]])

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        return np.array([[0.0]])
    
    def __repr__(self):
        return self.__doc__ 


""" --- Shape functions 1D --- """
class LagrangeLine2:
    """
    Shape functions for:
        dim: 1
        formulation: Lagrange
        element: Line
        n_nodes: 2
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]

        N1 = (1 - xi) / 2
        N2 = (1 + xi) / 2
        N = np.array([N1, N2])
        return N[np.newaxis].T

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        dN11 = -0.5
        dN21 = 0.5
        dN = np.array([dN11, dN21])
        return dN[np.newaxis].T
    
    def __repr__(self):
        return self.__doc__ 
    

class LagrangeLine3:
    """
    Shape functions for: 
        dim: 1
        formulation: Lagrange
        element: Line
        n_nodes: 3
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]

        N1 = xi * (xi - 1) / 2
        N2 = xi * (xi + 1) / 2
        N3 = (1 - xi**2)
        N = np.array([N1, N2, N3])
        return N[np.newaxis].T

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]

        dN11 = xi - 0.5
        dN21 = xi + 0.5
        dN31 = -2 * xi
        dN = np.array([dN11, dN21, dN31])
        return dN[np.newaxis].T

    def __repr__(self):
        return self.__doc__     


class LagrangeLine4:
    """
    Shape functions for: 
        dim: 1
        formulation: Lagrange
        element: Line
        n_nodes: 4
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]

        N1 = -9/16 * (xi + 1/3) * (xi - 1/3) * (xi - 1)
        N2 = 9/16 * (xi + 1) * (xi + 1/3) * (xi - 1/3)
        N3 = 27/16 * (xi + 1) * (xi - 1/3) * (xi - 1)
        N4 = -27/16 * (xi + 1) * (xi + 1/3) * (xi - 1)
        N = np.array([N1, N2, N3, N4])
        return N[np.newaxis].T

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]

        dN11 = -9/16 * ((xi - 1/3)*(xi - 1) + (xi + 1/3)*(xi - 1) + (xi + 1/3)*(xi - 1/3))
        dN21 = 9/16 * ((xi + 1/3)*(xi - 1/3) + (xi + 1)*(xi - 1/3) + (xi + 1)*(xi + 1/3))
        dN31 = 27/16 * ((xi - 1/3)*(xi - 1) + (xi + 1)*(xi - 1) + (xi + 1)*(xi - 1/3))
        dN41 = -27/16 * ((xi + 1/3)*(xi - 1) + (xi + 1)*(xi - 1) + (xi + 1)*(xi + 1/3))
        dN = np.array([dN11, dN21, dN31, dN41])
        return dN[np.newaxis].T
    
    def __repr__(self):
        return self.__doc__


class LagrangeLine5:
    """
    Shape functions for:
        dim: 1
        formulation: Lagrange
        element: Line
        n_nodes: 5
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]
        
        N1 = 2/3 * (xi - 1) * (xi + 0.5) * xi * (xi - 0.5)
        N2 = 2/3 * (xi + 1) * (xi + 0.5) * xi * (xi - 0.5)
        N3 = -8/3 * (xi + 1) * (xi - 1) * xi * (xi - 0.5) 
        N4 = 4 * (xi + 1) * (xi - 1) * (xi + 0.5) * (xi - 0.5)
        N5 = -8/3 * (xi + 1) * (xi - 1) * (xi + 0.5) * xi
        N = np.array([N1, N2, N3, N4, N5])
        return N[np.newaxis].T

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]

        dN11 = 2/3 * ((xi + 0.5)*(xi - 0.5)*(xi - 1) + (xi)*(xi - 0.5)*(xi - 1) + (xi + 0.5)*(xi)*(xi - 1) + (xi + 0.5)*(xi)*(xi - 0.5))
        dN21 = 2/3 * ((xi + 0.5)*(xi)*(xi - 0.5) + (xi + 1)*(xi)*(xi - 0.5) + (xi + 1)*(xi - 0.5)*(xi + 0.5) + (xi + 1)*(xi + 0.5)*(xi))
        dN31 = -8/3 * ((xi - 1)*(xi)*(xi - 0.5) + (xi + 1)*xi*(xi - 0.5) + (xi + 1)*(xi - 1)*(xi - 0.5) + (xi + 1)*(xi - 1)*xi)
        dN41 = 4 * ((xi - 1)*(xi + 0.5)*(xi - 0.5) + (xi + 1)*(xi + 0.5)*(xi - 0.5) + (xi + 1)*(xi - 1)*(xi - 0.5) + (xi + 1)*(xi - 1)*(xi + 0.5))
        dN51 = -8/3 * ((xi - 1)*(xi + 0.5)*xi + (xi + 1)*(xi + 0.5)*xi + (xi + 1)*(xi - 1)*xi + (xi + 1)*(xi - 1)*(xi + 0.5))
        dN = np.array([dN11, dN21, dN31, dN41, dN51])
        return dN[np.newaxis].T
    
    def __repr__(self):
        return self.__doc__
  

class LagrangeLine6:
    """
    Shape functions for:
        dim: 1
        formulation: Lagrange
        element: Line
        n_nodes: 6
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]

        N1 = (-625/768)*(xi + 3/5)*(xi + 1/5)*(xi - 1/5)*(xi - 3/5)*(xi - 1)
        N2 = (625/768)*(xi + 1)*(xi + 3/5)*(xi + 1/5)*(xi - 1/5)*(xi - 3/5)
        N3 = (3125/768)*(xi + 1)*(xi + 1/5)*(xi - 1/5)*(xi - 3/5)*(xi - 1)
        N4 = (-3125/384)*(xi + 1)*(xi + 3/5)*(xi - 1/5)*(xi - 3/5)*(xi - 1)
        N5 = (3125/384)*(xi + 1)*(xi + 3/5)*(xi + 1/5)*(xi - 3/5)*(xi - 1)
        N6 = (-3125/768)*(xi + 1)*(xi + 3/5)*(xi + 1/5)*(xi - 1/5)*(xi - 1)

        N = np.array([N1, N2, N3, N4, N5, N6])
        return N[np.newaxis].T

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]

        dN11 = (-625/768)*((xi + 1/5)*(xi - 1/5)*(xi - 3/5)*(xi - 1) + (xi + 3/5)*(xi - 1/5)*(xi - 3/5)*(xi - 1) + (xi + 3/5)*(xi + 1/5)*(xi - 3/5)*(xi - 1) + (xi + 3/5)*(xi + 1/5)*(xi - 1/5)*(xi - 1) + (xi + 3/5)*(xi + 1/5)*(xi - 1/5)*(xi - 3/5))
        dN21 = (625/768)*((xi + 3/5)*(xi + 1/5)*(xi - 1/5)*(xi - 3/5) + (xi + 1)*(xi + 1/5)*(xi - 1/5)*(xi - 3/5) + (xi + 1)*(xi + 3/5)*(xi - 1/5)*(xi - 3/5) + (xi + 1)*(xi + 3/5)*(xi + 1/5)*(xi - 3/5) + (xi + 1)*(xi + 3/5)*(xi + 1/5)*(xi - 1/5))
        dN31 = (3125/768)*((xi + 1/5)*(xi - 1/5)*(xi - 3/5)*(xi - 1) + (xi + 1)*(xi - 1/5)*(xi - 3/5)*(xi - 1) + (xi + 1)*(xi + 1/5)*(xi - 3/5)*(xi - 1) + (xi + 1)*(xi + 1/5)*(xi - 1/5)*(xi - 1) + (xi + 1)*(xi + 1/5)*(xi - 1/5)*(xi - 3/5))
        dN41 = (-3125/384)*((xi + 3/5)*(xi - 1/5)*(xi - 3/5)*(xi - 1) + (xi + 1)*(xi - 1/5)*(xi - 3/5)*(xi - 1) + (xi + 1)*(xi + 3/5)*(xi - 3/5)*(xi - 1) + (xi + 1)*(xi + 3/5)*(xi - 1/5)*(xi - 1) + (xi + 1)*(xi + 3/5)*(xi - 1/5)*(xi - 3/5))
        dN51 = (3125/384)*((xi + 3/5)*(xi + 1/5)*(xi - 3/5)*(xi - 1) + (xi + 1)*(xi + 1/5)*(xi - 3/5)*(xi - 1) + (xi + 1)*(xi + 3/5)*(xi - 3/5)*(xi - 1) + (xi + 1)*(xi + 3/5)*(xi + 1/5)*(xi - 1) + (xi + 1)*(xi + 3/5)*(xi + 1/5)*(xi - 3/5))
        dN61 = (-3125/768)*((xi + 3/5)*(xi + 1/5)*(xi - 1/5)*(xi - 1) + (xi + 1)*(xi + 1/5)*(xi - 1/5)*(xi - 1) + (xi + 1)*(xi + 3/5)*(xi - 1/5)*(xi - 1) + (xi + 1)*(xi + 3/5)*(xi + 1/5)*(xi - 1) + (xi + 1)*(xi + 3/5)*(xi + 1/5)*(xi - 1/5))
        dN = np.array([dN11, dN21, dN31, dN41, dN51, dN61])
        return dN[np.newaxis].T

    def __repr__(self):
        return self.__doc__


""" --- Shape functions 2D --- """
class LagrangeQuad4:
    """
    Shape functions for:
        dim: 2
        formulation: Lagrange
        element: Quadrilateral
        n_nodes: 4
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]
        eta = x[1]
        
        N1 = 0.25 * (1 - xi) * (1 - eta)
        N2 = 0.25 * (1 + xi) * (1 - eta)
        N3 = 0.25 * (1 + xi) * (1 + eta)
        N4 = 0.25 * (1 - xi) * (1 + eta)
        
        N = np.array([N1, N2, N3, N4])
        return N[np.newaxis].T

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]
        eta = x[1]
        
        dN_dxi = np.array([
            -0.25 * (1 - eta),
             0.25 * (1 - eta),
             0.25 * (1 + eta),
            -0.25 * (1 + eta)
        ])
        
        dN_deta = np.array([
            -0.25 * (1 - xi),
            -0.25 * (1 + xi),
             0.25 * (1 + xi),
             0.25 * (1 - xi)
        ])
        
        dN = np.column_stack((dN_dxi, dN_deta))
        return dN
    
    def __repr__(self):
        return self.__doc__


class LagrangeQuad9:
    """
    Shape functions for:
        dim: 2
        formulation: Lagrange
        element: Quadrilateral
        n_nodes: 9
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]
        eta = x[1]
        
        N1 = 0.25 * (xi - 1) * (eta - 1) * xi * eta
        N2 = 0.25 * (xi + 1) * (eta - 1) * xi * eta
        N3 = 0.25 * (xi + 1) * (eta + 1) * xi * eta
        N4 = 0.25 * (xi - 1) * (eta + 1) * xi * eta
        N5 = 0.5 * (1 - xi**2) * (eta - 1) * eta
        N6 = 0.5 * (xi + 1) * xi * (1 - eta**2)
        N7 = 0.5 * (1 - xi**2) * (eta + 1) * eta
        N8 = 0.5 * (xi - 1) * xi * (1 - eta**2)
        N9 = (1 - xi**2) * (1 - eta**2)
        
        N = np.array([N1, N2, N3, N4, N5, N6, N7, N8, N9])
        return N[np.newaxis].T

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]
        eta = x[1]
        
        dN_dxi = np.array([
            0.25 * (2*xi - 1) * (eta - 1) * eta,
            0.25 * (2*xi + 1) * (eta - 1) * eta,
            0.25 * (2*xi + 1) * (eta + 1) * eta,
            0.25 * (2*xi - 1) * (eta + 1) * eta,
            -xi * (eta - 1) * eta,
            0.5 * (2*xi + 1) * (1 - eta**2),
            -xi * (eta + 1) * eta,
            0.5 * (2*xi - 1) * (1 - eta**2),
            -2 * xi * (1 - eta**2)
        ])
        dN_deta = np.array([
            0.25 * (xi - 1) * (2*eta - 1) * xi,
            0.25 * (xi + 1) * (2*eta - 1) * xi,
            0.25 * (xi + 1) * (2*eta + 1) * xi,
            0.25 * (xi - 1) * (2*eta + 1) * xi,
            0.5 * (1 - xi**2) * (2*eta - 1),
            -eta * (xi + 1) * xi,
            0.5 * (1 - xi**2) * (2*eta + 1),
            -eta * (xi - 1) * xi,
            -2 * eta * (1 - xi**2)
        ])
        
        dN = np.column_stack((dN_dxi, dN_deta))
        return dN
    
    def __repr__(self):
        return self.__doc__


class LagrangeQuad8:
    """
    Shape functions for:
        dim: 2
        formulation: Lagrange
        element: Quadrilateral
        n_nodes: 8
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]
        eta = x[1]
        
        N1 = 0.25 * (1 - xi) * (1 - eta) * (-xi - eta - 1)
        N2 = 0.25 * (1 + xi) * (1 - eta) * (xi - eta - 1)
        N3 = 0.25 * (1 + xi) * (1 + eta) * (xi + eta - 1)
        N4 = 0.25 * (1 - xi) * (1 + eta) * (-xi + eta - 1)
        N5 = 0.5 * (1 - xi**2) * (1 - eta)
        N6 = 0.5 * (1 + xi) * (1 - eta**2)
        N7 = 0.5 * (1 - xi**2) * (1 + eta)
        N8 = 0.5 * (1 - xi) * (1 - eta**2)
        
        N = np.array([N1, N2, N3, N4, N5, N6, N7, N8])
        return N[np.newaxis].T

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]
        eta = x[1]
        
        dN_dxi = np.array([
            0.25 * (1 - eta) * (2*xi + eta), # 
            0.25 * (1 - eta) * (2*xi - eta), # 
            0.25 * (1 + eta) * (2*xi + eta), #
            0.25 * (1 + eta) * (2*xi - eta), #
            -xi * (1 - eta),
            0.5 * (1 - eta**2),
            -xi * (1 + eta),
            -0.5 * (1 - eta**2)
        ])
        dN_deta = np.array([
            0.25 * (1 - xi) * (xi + 2*eta), #
            0.25 * (1 + xi) * (-xi + 2*eta), # 
            0.25 * (1 + xi) * (xi + 2*eta), #
            0.25 * (1 - xi) * (-xi + 2*eta), #
            -0.5 * (1 - xi**2),
            -eta * (1 + xi),
            0.5 * (1 - xi**2),
            -eta * (1 - xi)
        ])

        dN = np.column_stack((dN_dxi, dN_deta))
        return dN
    
    def __repr__(self):
        return self.__doc__


class LagrangeTri3:
    """
    Shape functions for:
        dim: 2
        formulation: Lagrange
        element: Triangle
        n_nodes: 3
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]
        eta = x[1]
        
        N1 = 1 - xi - eta
        N2 = xi
        N3 = eta
        
        N = np.array([N1, N2, N3])
        return N[np.newaxis].T

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        dN_dxi = np.array([-1, 1, 0])
        dN_deta = np.array([-1, 0, 1])
        
        dN = np.column_stack((dN_dxi, dN_deta))
        return dN
    
    def __repr__(self):
        return self.__doc__
    

class LagrangeTri6:
    """
    Shape functions for:
        dim: 2
        formulation: Lagrange
        element: Triangle
        n_nodes: 6
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]
        eta = x[1]
        zeta = 1 - xi - eta
        
        N1 = zeta * (2 * zeta - 1)
        N2 = xi * (2 * xi - 1)
        N3 = eta * (2 * eta - 1)
        N4 = 4 * xi * zeta
        N5 = 4 * xi * eta
        N6 = 4 * eta * zeta
        
        N = np.array([N1, N2, N3, N4, N5, N6])
        return N[np.newaxis].T

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]
        eta = x[1]
        zeta = 1 - xi - eta
        
        dN_dxi = np.array([
            - (4 * zeta - 1),
            4 * xi - 1,
            0,
            4 * (zeta - xi),
            4 * eta,
            -4 * eta
        ])
        
        dN_deta = np.array([
            - (4 * zeta - 1),
            0,
            4 * eta - 1,
            -4 * xi,
            4 * xi,
            4 * (zeta - eta)
        ])
        
        dN = np.column_stack((dN_dxi, dN_deta))
        return dN
    
    def __repr__(self):
        return self.__doc__
    

class LagrangeTri10:
    """
    Shape functions for:
        dim: 2
        formulation: Lagrange
        element: Triangle
        n_nodes: 10
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]
        eta = x[1]
        zeta = 1 - xi - eta
        
        N1 = (1/2) * zeta * (3 * zeta - 1) * (3 * zeta - 2)
        N2 = (1/2) * xi * (3 * xi - 1) * (3 * xi - 2)
        N3 = (1/2) * eta * (3 * eta - 1) * (3 * eta - 2)
        N4 = (9/2) * xi * zeta * (3 * zeta - 1)
        N5 = (9/2) * xi * zeta * (3 * xi - 1)
        N6 = (9/2) * xi * eta * (3 * xi - 1)
        N7 = (9/2) * xi * eta * (3 * eta - 1)
        N8 = (9/2) * eta * zeta * (3 * eta - 1)
        N9 = (9/2) * eta * zeta * (3 * zeta - 1)
        N10 = 27 * xi * eta * zeta
        
        N = np.array([N1, N2, N3, N4, N5, N6, N7, N8, N9, N10])
        return N[np.newaxis].T
    
    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]
        eta = x[1]
        zeta = 1 - xi - eta
        
        dN_dxi = np.array([
            -0.5 * (27*zeta**2 - 18*zeta + 2),
            0.5 * (27*xi**2   - 18*xi   + 2),
            0.0,
            4.5 * (zeta*(3*zeta - 1) - xi*(6*zeta - 1)),
            4.5 * (zeta*(6*xi - 1)   - xi*(3*xi - 1)),
            4.5 * eta*(6*xi - 1),
            4.5 * eta*(3*eta - 1),
            -4.5 * eta*(3*eta - 1),
            -4.5 * eta*(6*zeta - 1),
            27 * eta * (zeta - xi)
        ])
        
        dN_deta = np.array([
            -0.5 * (27*zeta**2 - 18*zeta + 2),
            0.0,
            0.5 * (27*eta**2 - 18*eta + 2),
            -4.5 * xi*(6*zeta - 1),
            -4.5 * xi*(3*xi - 1),
            4.5 * xi*(3*xi - 1),
            4.5 * xi*(6*eta - 1),
            4.5 * (zeta*(6*eta - 1) - eta*(3*eta - 1)),
            4.5 * (zeta*(3*zeta - 1) - eta*(6*zeta - 1)),
            27 * xi * (zeta - eta)
        ])
        
        dN = np.column_stack((dN_dxi, dN_deta))
        return dN


""" --- Shape functions 3D --- """
class LagrangeTet4:
    """
    Shape functions for:
        dim: 3
        formulation: Lagrange
        element: Tetrahedron
        n_nodes: 4
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]
        eta = x[1]
        zeta = x[2]
        gamma = 1 - xi - eta - zeta
        
        N1 = gamma
        N2 = xi
        N3 = eta
        N4 = zeta
        
        N = np.array([N1, N2, N3, N4])
        return N[np.newaxis].T

    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        dN_dxi = np.array([
            -1,
            1,
            0,
            0
        ])

        dN_deta = np.array([
            -1,
            0,
            1,
            0
        ])

        dN_dzeta = np.array([
            -1,
            0,
            0,
            1
        ])

        dN = np.column_stack((dN_dxi, dN_deta, dN_dzeta))
        return dN
    

class LagrangeHex8:
    """
    Shape functions for:
        dim: 3
        formulation: Lagrange
        element: Hexahedron
        n_nodes: 8
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]
        eta = x[1]
        zeta = x[2]
        
        N1 = 0.125 * (1 - xi) * (1 - eta) * (1 - zeta)
        N2 = 0.125 * (1 + xi) * (1 - eta) * (1 - zeta)
        N3 = 0.125 * (1 + xi) * (1 + eta) * (1 - zeta)
        N4 = 0.125 * (1 - xi) * (1 + eta) * (1 - zeta)
        N5 = 0.125 * (1 - xi) * (1 - eta) * (1 + zeta)
        N6 = 0.125 * (1 + xi) * (1 - eta) * (1 + zeta)
        N7 = 0.125 * (1 + xi) * (1 + eta) * (1 + zeta)
        N8 = 0.125 * (1 - xi) * (1 + eta) * (1 + zeta)
        
        N = np.array([N1, N2, N3, N4, N5, N6, N7, N8])
        return N[np.newaxis].T
    
    @staticmethod
    def dShape(x):
        """ Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]
        eta = x[1]
        zeta = x[2]
        
        dN_dxi = np.array([
            -0.125 * (1 - eta) * (1 - zeta),
             0.125 * (1 - eta) * (1 - zeta),
             0.125 * (1 + eta) * (1 - zeta),
            -0.125 * (1 + eta) * (1 - zeta),
            -0.125 * (1 - eta) * (1 + zeta),
             0.125 * (1 - eta) * (1 + zeta),
             0.125 * (1 + eta) * (1 + zeta),
            -0.125 * (1 + eta) * (1 + zeta)
        ])
        
        dN_deta = np.array([
            -0.125 * (1 - xi) * (1 - zeta),
            -0.125 * (1 + xi) * (1 - zeta),
             0.125 * (1 + xi) * (1 - zeta),
             0.125 * (1 - xi) * (1 - zeta),
            -0.125 * (1 - xi) * (1 + zeta),
            -0.125 * (1 + xi) * (1 + zeta),
             0.125 * (1 + xi) * (1 + zeta),
             0.125 * (1 - xi) * (1 + zeta)
        ])
        
        dN_dzeta = np.array([
            -0.125 * (1 - xi) * (1 - eta),
            -0.125 * (1 + xi) * (1 - eta),
            -0.125 * (1 + xi) * (1 + eta),
            -0.125 * (1 - xi) * (1 + eta),
             0.125 * (1 - xi) * (1 - eta),
             0.125 * (1 + xi) * (1 - eta),
             0.125 * (1 + xi) * (1 + eta),
             0.125 * (1 - xi) * (1 + eta)
        ])
        
        dN = np.column_stack((dN_dxi, dN_deta, dN_dzeta))
        return dN


class LagrangePrism6:
    """
    Shape functions for:
        dim: 3
        formulation: Lagrange
        element: Prism
        n_nodes: 6
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]
        eta = x[1]
        zeta = x[2]
        
        N1 = 0.5 * (1 - xi - eta) * (1 - zeta)
        N2 = 0.5 * xi * (1 - zeta)
        N3 = 0.5 * eta * (1 - zeta)
        N4 = 0.5 * (1 - xi - eta) * (1 + zeta)
        N5 = 0.5 * xi * (1 + zeta)
        N6 = 0.5 * eta * (1 + zeta)
        
        N = np.array([N1, N2, N3, N4, N5, N6])
        return N[np.newaxis].T
    
    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]
        eta = x[1]
        zeta = x[2]
        
        dN_dxi = np.array([
            -0.5 * (1 - zeta),
             0.5 * (1 - zeta),
             0,
            -0.5 * (1 + zeta),
             0.5 * (1 + zeta),
             0
        ])
        
        dN_deta = np.array([
            -0.5 * (1 - zeta),
            0,
             0.5 * (1 - zeta),
            -0.5 * (1 + zeta),
            0,
             0.5 * (1 + zeta)
        ])
        
        dN_dzeta = np.array([
            -0.5 * (1 - xi - eta),
            -0.5 * xi,
            -0.5 * eta,
             0.5 * (1 - xi - eta),
             0.5 * xi,
             0.5 * eta
        ])
        
        dN = np.column_stack((dN_dxi, dN_deta, dN_dzeta))
        return dN


class LagrangePyram5:
    """
    Shape functions for:
        dim: 3
        formulation: Lagrange
        element: Pyramid
        n_nodes: 5
    """
    @staticmethod
    def shape(x):
        """Returns shape functions"""
        xi = x[0]
        eta = x[1]
        zeta = x[2]

        N1 = 0.25 * (1 - xi) * (1 - eta) * (1 - zeta)
        N2 = 0.25 * (1 + xi) * (1 - eta) * (1 - zeta)
        N3 = 0.25 * (1 + xi) * (1 + eta) * (1 - zeta)
        N4 = 0.25 * (1 - xi) * (1 + eta) * (1 - zeta)
        N5 = zeta
        N = np.array([N1, N2, N3, N4, N5])
        return N[np.newaxis].T
    
    @staticmethod
    def dShape(x):
        """Returns derivatives of shape functions (with respect to reference coordinates)"""
        xi = x[0]
        eta = x[1]
        zeta = x[2]

        dN_dxi = np.array([
            -0.25 * (1 - eta) * (1 - zeta),
             0.25 * (1 - eta) * (1 - zeta),
             0.25 * (1 + eta) * (1 - zeta),
            -0.25 * (1 + eta) * (1 - zeta),
             0
        ])

        dN_deta = np.array([
            -0.25 * (1 - xi) * (1 - zeta),
            -0.25 * (1 + xi) * (1 - zeta),
             0.25 * (1 + xi) * (1 - zeta),
             0.25 * (1 - xi) * (1 - zeta),
             0
        ])

        dN_dzeta = np.array([
            -0.25 * (1 - xi) * (1 - eta),
            -0.25 * (1 + xi) * (1 - eta),
            -0.25 * (1 + xi) * (1 + eta),
            -0.25 * (1 - xi) * (1 + eta),
             1
        ])

        dN = np.column_stack((dN_dxi, dN_deta, dN_dzeta))
        return dN

        

