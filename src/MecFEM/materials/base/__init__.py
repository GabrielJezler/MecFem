from .non_linear_isotropic import NonLinearIsotropic
from .linear_isotropic import LinearIsotropic

Material = LinearIsotropic | NonLinearIsotropic

__all__ = ['LinearIsotropic', 'NonLinearIsotropic']