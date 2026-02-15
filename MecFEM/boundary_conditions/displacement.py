import numpy as np

class Displacement:
    """
    Data structure for displacement field applied to the FE model.
    
    Attributes
    ----------
    field : Function
        Function that defines the displacement field as a function of spatial coordinates x.
    """
    def __init__(self, field) -> None:
        if not callable(field):
            raise TypeError("field must be a callable function")

        self._field = field

    def __call__(self, x_nodes: np.ndarray | None=None) -> np.ndarray:
        """
        It evaluates the displacement field at the integration points.

        Parameters
        ----------
        x_nodes : ndarray | None
            Coordinates of the element nodes if provided. This is an array of shape (n_nodes, dim).
        
        Returns
        -------
        u_int_pts : ndarray
            Displacement vector at the integration points. This is an array of shape (n_int_pts, dim).
        """
        return self._field(x_nodes)
    
    def __add__(self, other):
        if isinstance(other, Displacement):        
            def combined_field(x):
                return self._field(x) + other._field(x)
            
            return Displacement(combined_field)
        else:
            raise TypeError("Can only add ForceField instances")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            def scaled_field(x):
                return scalar * self._field(x)
            
            return Displacement(scaled_field)
        else:
            raise TypeError("Can only multiply by a scalar (int or float)")
        
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            def divided_field(x):
                return self._field(x) / scalar
            
            return Displacement(divided_field)
        else:
            raise TypeError("Can only divide by a scalar (int or float)")
