import numpy as np

class VolumetricForce:
    """
    Data structure for volumetric force field applied to the FE model.
    
    Attributes
    ----------
    field : Function
        Function that defines the volumetric force field as a function of spatial coordinates x.
    """
    def __init__(self, field) -> None:
        if not callable(field):
            raise TypeError("field must be a callable function")

        self._field = field

    def __call__(self, x_nodes: np.ndarray, f_shape: np.ndarray) -> np.ndarray:
        """
        It evaluates the volumetric force field at the integration points.

        Parameters
        ----------
        x_nodes : ndarray
            Coordinates of the element nodes. This is an array of shape (n_nodes, dim).
        f_shape : ndarray
            Shape functions evaluated at the integration points. This is an array of shape (n_int_pts, n_nodes, 1).
        
        Returns
        -------
        f_int_pts : ndarray
            Volumetric force vector at the integration points. This is an array of shape (n_int_pts, dim).
        """
        x_int_pts = np.einsum('ni,ik->nk', f_shape[:,:,0],  x_nodes)

        f_int_pts = self._field(x_int_pts)
        return f_int_pts
    
    def __add__(self, other):
        if isinstance(other, VolumetricForce):        
            def combined_field(x):
                return self._field(x) + other._field(x)
            
            return VolumetricForce(combined_field)
        else:
            raise TypeError("Can only add ForceField instances")

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            def scaled_field(x):
                return scalar * self._field(x)
            
            return VolumetricForce(scaled_field)
        else:
            raise TypeError("Can only multiply by a scalar (int or float)")
        
    def __rmul__(self, scalar):
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            def divided_field(x):
                return self._field(x) / scalar
            
            return VolumetricForce(divided_field)
        else:
            raise TypeError("Can only divide by a scalar (int or float)")
    
