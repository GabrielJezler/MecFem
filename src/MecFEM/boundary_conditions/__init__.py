from .step import BCStep

from .volumetric_force import VolumetricForce
from .displacement import Displacement

Field = VolumetricForce | Displacement

from . import functions