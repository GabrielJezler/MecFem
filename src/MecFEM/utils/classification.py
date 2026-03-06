from enum import Enum

class MaterialBehavior(Enum):
    """
    Enumerator for material behavior.
    """
    ELASTIC = "Elastic"
    PLASTIC = "Plastic"
    VISCOUS = "Viscous"

class MaterialSymmetry(Enum):
    """
    Enumerator for material symmetry.
    """
    ISOTROPIC = "Isotropic"
    ORTHOTROPIC = "Orthotropic"
    ANISOTROPIC = "Anisotropic"

class SolverClassification(Enum):
    """
    Enumerator for solver classification.
    """
    NONE = "None"
    LINEAR = "Linear"
    NON_LINEAR = "Non-linear"