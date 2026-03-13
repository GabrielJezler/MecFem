from dataclasses import dataclass, field
import flet as ft

from .data import SpotData

@ft.observable
@dataclass
class ChartState:
    selected: list[int] = field(default_factory=list)
    spots: list[SpotData] = field(default_factory=list)

    def update_selected(self, indices: list[int]):
        self.selected = indices

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
