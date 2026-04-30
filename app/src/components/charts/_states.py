from dataclasses import dataclass, field
import numpy as np
import flet as ft

from ._data import SpotData

@ft.observable
@dataclass
class ChartState:
    spots_selected: list[int] = field(default_factory=list)
    spots: list[SpotData] = field(default_factory=list)
    elements_selected: list[int] = field(default_factory=list)
    elements: list[list[float]] = field(default_factory=list)
    size:dict[str, float] = field(default_factory=lambda: {"width": 1.0, "height": 1.0})

    def update_size(self, width: float, height: float):
        self.size["width"] = width
        self.size["height"] = height

    def update_spots_selection(self, indices: list[int]):
        print(f"Selected spots: {indices}")
        self.spots_selected = indices

    def update_elements_selection(self, indices: list[int]):
        print(f"Selected elements: {indices}")
        self.elements_selected = indices

@ft.observable
@dataclass
class SelectionBoxState:
    x0: float = 0.0
    y0: float = 0.0
    x1: float = 0.0
    y1: float = 0.0

    def set_initial_position(self, x: float, y: float):
        self.x0 = x
        self.y0 = y

        self.x1 = x
        self.y1 = y
    
    def update_final_position(self, dx: float, dy: float):
        self.x1 = self.x1 + dx
        self.y1 = self.y1 + dy

    def reset(self):
        self.x0 = 0.0
        self.y0 = 0.0
        self.x1 = 0.0
        self.y1 = 0.0
