from dataclasses import dataclass
import flet as ft

@dataclass
class SpotData:
    x: float
    y: float
    color: ft.Colors | str
    selected_color: ft.Colors |str
    radius: float = 8.0
    id: int | None = None
