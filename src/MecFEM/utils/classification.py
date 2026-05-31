from enum import Enum
from dataclasses import dataclass
from typing import Any

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

class BoundaryConditionObject(Enum):
    """
    Enumerator for boundary condition regions.
    """
    NODES = "Nodes"
    ELEMENTS = "Elements"

class BoundaryConditionRegion(Enum):
    """
    Enumerator for boundary condition regions.
    """
    BOUNDARY = "Boundary"
    VOLUME = "Volume"

class BoundaryConditionName(Enum):
    """
    Enumerator for boundary condition types.
    """
    DISPLACEMENT = "Displacement"
    VOLUMETRIC_FORCE = "Volumetric Force"
    # The BC below are not yet supported
    EXTERNAL_FORCE = "External Force"
    TEMPERATURE = "Temperature"

@dataclass
class BoundaryConditionClass:
    """
    Data class for boundary condition classification.
    """
    object: list[BoundaryConditionObject]
    region:list[BoundaryConditionRegion]
    name: BoundaryConditionName

class BoundaryConditionClassification(Enum):
    """
    Enumerator for boundary condition classification.
    """
    DISPLACEMENT = BoundaryConditionClass(
        object=[BoundaryConditionObject.NODES],
        region=[BoundaryConditionRegion.BOUNDARY, BoundaryConditionRegion.VOLUME],
        name=BoundaryConditionName.DISPLACEMENT,
    )
    VOLUMETRIC_FORCE = BoundaryConditionClass(
        object=[BoundaryConditionObject.ELEMENTS],
        region=[BoundaryConditionRegion.VOLUME],
        name=BoundaryConditionName.VOLUMETRIC_FORCE
    )
    # The BC below are not yet supported
    EXTERNAL_FORCE = BoundaryConditionClass(
        object=[BoundaryConditionObject.ELEMENTS],
        region=[BoundaryConditionRegion.BOUNDARY],
        name=BoundaryConditionName.EXTERNAL_FORCE
    )
    TEMPERATURE = BoundaryConditionClass(
        object=[BoundaryConditionObject.NODES, BoundaryConditionObject.ELEMENTS],
        region=[BoundaryConditionRegion.VOLUME],
        name=BoundaryConditionName.TEMPERATURE
    )
