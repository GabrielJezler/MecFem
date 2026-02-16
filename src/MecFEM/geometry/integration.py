import numpy as np
import math

# References:
# https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v251/en/ans_thry/thy_et1.html

""" --- Integration points 0D --- """
class GaussPoint:
    """
    Numerical integration rules for point element
    
    Attributes
    ----------
    N : int
        Total number of integration points
    X : np.ndarray
        Coordinates of integration points. This is an array of shape (N, 1).
    W : np.ndarray
        Weights of integration points. This is an array of shape (N,).
    """
    def __init__(self, N: int=1):
        """
        Gives the coordinates and weights of the 0D Gauss integration point.

        Parameters
        ----------
        N : int
            Number of integration points. Only 1 is supported.
        
        Returns
        -------
        None.
        """
        if not isinstance(N, int):
            raise TypeError("Number of integration points N must be an integer.")
        if N != 1:
            raise ValueError("GaussPoint only supports order 1 for a Point element.")
        
        self.N = N
        self.X = np.array([[0.0]])  # coordinates of integration point
        self.W = np.array([1.0])     # weight

    def possible_integration_numbers(self) -> list[int] | None:
        """
        Get possible number of integration points for a point element.

        Returns
        -------
        possible: list[int] | None
            List of possible number of integration points. None if an infinite number of integration points is possible.
        """
        possible = [1]
        return possible


""" --- Integration points 1D --- """
class GaussLine:
    """
    Numerical integration rules for line segment
    
    Attributes
    ----------
    N : int
        Total number of integration points
    X : np.ndarray
        Coordinates of integration points. This is an array of shape (N, 1).
    W : np.ndarray
        Weights of integration points. This is an array of shape (N,).
    """
    def __init__(self, N: int=2):
        """
        Gives the coordinates and weights of the 1D Gauss integration points.

        Parameters
        ----------
        N : int
            Number of integration points along the line segment.
        
        Returns
        -------
        None.
        """
        if not isinstance(N, int):
            raise TypeError("Number of integration points N must be an integer.")
        if N < 1:
            raise ValueError("Number of integration points N must be at least 1.")

        self.N = N
        self.X, self.W = np.polynomial.legendre.leggauss(self.N)
        self.X = self.X[np.newaxis, :].T

    def possible_integration_numbers(self) -> list[int] | None:
        """
        Get possible number of integration points for a point element.

        Returns
        -------
        possible: list[int] | None
            List of possible number of integration points. None if an infinite number of integration points is possible.
        """
        possible = None
        return possible


""" --- Integration points 2D --- """
class GaussQuadrangle:
    """
    Numerical integration rules for quadrangles

    Attributes
    ----------
    N : int
        Total number of integration points
    X : np.ndarray
        Coordinates of integration points. This is an array of shape (N, 2).
    W : np.ndarray
        Weights of integration points. This is an array of shape (N,).
    """
    def __init__(self, N: int=4):
        """
        Gives the coordinates and weights of the 2D Gauss integration points
        for quadrilateral elements.

        Parameters
        ----------
        order: int
            Number of integration points along one dimension (total points will be n^2).

        Returns
        -------
        None.
        """
        if not isinstance(N, int):
            raise TypeError("Number of integration points N must be an integer.")
        if math.isqrt(N) ** 2 != N:
            raise ValueError("N must be a perfect square for GaussQuadrangle.")
        if N < 1:
            raise ValueError("Number of integration points N must be at least 1.")
        
        self.N = N
        x, wx = np.polynomial.legendre.leggauss(math.isqrt(N))  # 1D Gauss points and weights
        y, wy = np.polynomial.legendre.leggauss(math.isqrt(N))

        X, Y = np.meshgrid(x, y)  # Create 2D grid of points
        WX, WY = np.meshgrid(wx, wy)

        self.W = (WX * WY).ravel()  # Tensor product of weights
        self.X = np.column_stack([X.ravel(), Y.ravel()]) 

    def possible_integration_numbers(self) -> list[int] | None:
        """
        Get possible number of integration points for a point element.

        Returns
        -------
        possible: list[int] | None
            List of possible number of integration points. None if an infinite number of integration points is possible.
        """
        possible = None
        return possible
    

class GaussTriangle:
    """
    Numerical integration rules for triangular elements
    
    Attributes
    ----------
    N : int
        Total number of integration points
    X : np.ndarray
        Coordinates of integration points. This is an array of shape (N, 2).
    W : np.ndarray
        Weights of integration points. This is an array of shape (N,).
    """
    def __init__(self, N: int=3):
        """
        Gives the coordinates and weights of the 2D Gauss integration points
        for triangular elements.

        Parameters
        ----------
        N : int
            Order of the integration rule (1, 2, or 3).

        Returns
        -------
        None.
        """
        if not isinstance(N, int):
            raise TypeError("Number of integration points N must be an integer.")
        if N not in [1, 3, 6]:
            raise ValueError("Unsupported number of integration points for GaussTriangle. Supported values are 1, 3, and 6.")
        
        if N == 1:
            self.N = 1
            self.X = np.array([
                [1/3, 1/3]
            ])
            self.W = np.array([0.5])
        elif N == 3:
            self.N = 3
            self.X = np.array([
                [1/6, 1/6],
                [2/3, 1/6],
                [1/6, 2/3]
            ])
            self.W = np.array([1/6, 1/6, 1/6])
        elif N == 6:
            self.N = 6
            self.X = np.array([
                [0.445948490915965, 0.445948490915965],
                [0.445948490915965, 0.108103018168070],
                [0.108103018168070, 0.445948490915965],
                [0.091576213509771, 0.091576213509771],
                [0.091576213509771, 0.816847572980459],
                [0.816847572980459, 0.091576213509771],
            ])
            self.W = np.array([
                0.111690794839005,
                0.111690794839005,
                0.111690794839005,
                0.054975871827661,
                0.054975871827661,
                0.054975871827661,
            ])

    def possible_integration_numbers(self) -> list[int] | None:
        """
        Get possible number of integration points for a point element.

        Returns
        -------
        possible: list[int] | None
            List of possible number of integration points. None if an infinite number of integration points is possible.
        """
        possible = [1, 3, 6]
        return possible


""" --- Integration points 3D --- """
class GaussTetrahedron:
    """
    Numerical integration rules for tetrahedral elements
    
    Attributes
    ----------
    N : int
        Total number of integration points
    X : np.ndarray
        Coordinates of integration points. This is an array of shape (N, 3).
    W : np.ndarray
        Weights of integration points. This is an array of shape (N,).
    """
    def __init__(self, N=1):
        """
        Gives the coordinates and weights of the 3D Gauss integration points
        for tetrahedral elements.

        Parameters
        ----------
        N : int
            Number of integration points.

        Returns
        -------
        None.
        """
        self.N = N
        # ...

    def possible_integration_numbers(self) -> list[int] | None:
        """
        Get possible number of integration points for a point element.

        Returns
        -------
        possible: list[int] | None
            List of possible number of integration points. None if an infinite number of integration points is possible.
        """
        possible = [1]
        return possible


class GaussHexahedron:
    """
    Numerical integration rules for hexahedral elements
    
    Attributes
    ----------
    N : int
        Total number of integration points
    X : np.ndarray
        Coordinates of integration points. This is an array of shape (N, 3).
    W : np.ndarray
        Weights of integration points. This is an array of shape (N,).
    """
    def __init__(self, N=1):
        """
        Gives the coordinates and weights of the 3D Gauss integration points
        for hexahedral elements.

        Parameters
        ----------
        N : int
            Number of integration points.

        Returns
        -------
        None.
        """
        self.N = N
        # ...

    def possible_integration_numbers(self) -> list[int] | None:
        """
        Get possible number of integration points for a point element.

        Returns
        -------
        possible: list[int] | None
            List of possible number of integration points. None if an infinite number of integration points is possible.
        """
        possible = [1]
        return possible


class GaussPrism:
    """
    Numerical integration rules for prismatic elements
    
    Attributes
    ----------
    N : int
        Total number of integration points
    X : np.ndarray
        Coordinates of integration points. This is an array of shape (N, 3).
    W : np.ndarray
        Weights of integration points. This is an array of shape (N,).
    """
    def __init__(self, N=1):
        """
        Gives the coordinates and weights of the 3D Gauss integration points
        for prismatic elements.

        Parameters
        ----------
        N : int
            Number of integration points.

        Returns
        -------
        None.
        """
        self.N = N
        # ...

    def possible_integration_numbers(self) -> list[int] | None:
        """
        Get possible number of integration points for a point element.

        Returns
        -------
        possible: list[int] | None
            List of possible number of integration points. None if an infinite number of integration points is possible.
        """
        possible = [1]
        return possible


class GaussPyramid:
    """
    Numerical integration rules for pyramidal elements
    
    Attributes
    ----------
    N : int
        Total number of integration points
    X : np.ndarray
        Coordinates of integration points. This is an array of shape (N, 3).
    W : np.ndarray
        Weights of integration points. This is an array of shape (N,).
    """
    def __init__(self, N=1):
        """
        Gives the coordinates and weights of the 3D Gauss integration points
        for pyramidal elements.

        Parameters
        ----------
        N : int
            Number of integration points.

        Returns
        -------
        None.
        """
        self.N = N
        # ...

    def possible_integration_numbers(self) -> list[int] | None:
        """
        Get possible number of integration points for a point element.

        Returns
        -------
        possible: list[int] | None
            List of possible number of integration points. None if an infinite number of integration points is possible.
        """
        possible = [1]
        return possible

