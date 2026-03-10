import flet as ft
from dataclasses import dataclass

@ft.observable
@dataclass()
class Page:
    name: str
    route: str
    index:int
    icon: ft.Icon
    content: ft.Control
