from enum import Enum

class GestureSelectionMode(Enum):
    """
    Enumerator for different selection modes in the mesh chart.
    """
    NONE = "None"
    RECTANGLE = "Rectangle"
    LASSO = "Lasso"

class MeshSelectionMode(Enum):
    """
    Enumerator for different selection modes in the mesh chart.
    """
    NONE = "None"
    NODES = "Nodes"
    ELEMENTS = "Elements"
