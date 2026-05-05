from enum import Enum

class MeshSelectionShape(Enum):
    """
    Enumerator for different selection modes in the mesh chart.
    """
    NONE = "None"
    RECTANGLE = "Rectangle"
    LASSO = "Lasso"

class MeshSelectionObject(Enum):
    """
    Enumerator for different selection modes in the mesh chart.
    """
    NODES = "Nodes"
    ELEMENTS = "Elements"

class MeshSelectionZone(Enum):
    """
    Enumerator for different selection modes in the mesh chart.
    """
    BOUNDARY = "Boundary"
    VOLUME = "Volume"
