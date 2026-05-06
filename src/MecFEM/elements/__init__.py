from .non_linear import NonLinearFiniteElement
from .linear import LinearFiniteElement

FiniteElement = NonLinearFiniteElement | LinearFiniteElement

__all__ = ["NonLinearFiniteElement", "LinearFiniteElement"]