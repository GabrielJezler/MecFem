from enum import Enum

class GestureSelectionMode(Enum):
    """
    Enumerator for different selection modes in the mesh chart.
    """
    NONE = "None"
    RECTANGLE = "Rectangle"
    LASSO = "Lasso"