import flet as ft
from dataclasses import dataclass, field
from collections.abc import Callable
from typing import Dict

from structures.states import SimulationState
from utils import tomltools

from .enums import GestureSelectionMode
from .chart import SelectionData

@dataclass(frozen=True)
class ThemeContextValue:
    mode: ft.ThemeMode
    toggle: Callable[[], None]
    _colors: Dict[str, str] = field(default_factory=lambda: tomltools.load_colors())
    _config: Dict[str, str] = field(default_factory=lambda: tomltools.load_config())

    @property
    def colors(self):
        return self._colors[self.mode.value]

    @property
    def config(self):
        return self._config


@dataclass
class SimulationContextValue:
    state: SimulationState

ThemeContext = ft.create_context(ThemeContextValue(ft.ThemeMode.LIGHT, lambda: None))

SimulationContext = ft.create_context(SimulationContextValue(SimulationState()))

OrientationContext = ft.create_context(ft.Orientation.LANDSCAPE)

SelectionDataContext = ft.create_context(SelectionData())
