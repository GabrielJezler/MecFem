import flet as ft
import asyncio
from dataclasses import dataclass
from typing import Any

import MecFEM as mf

from utils import tomltools

@ft.observable
@dataclass
class SimulationState:
    material: Any = None
    mesh_path: str = None
    mesh: mf.mesh.Mesh | None = None
    model: Any = None
    ran: bool = False

    def __repr__(self):
        return f"SimulationData(material={self.material}, mesh={self.mesh}, model={self.model}, ran={self.ran})"

@ft.observable
@dataclass
class AppState:
    route: str
    theme_mode: ft.ThemeMode
    colors: dict
    config: dict
    simulation_data: SimulationState

    def toggle_theme(self):
        self.theme_mode = (
            ft.ThemeMode.DARK
            if self.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        
        self.config["theme"]["mode"] = "dark" if self.theme_mode == ft.ThemeMode.DARK else "light"
        tomltools.update_config(self.config)

    def route_change(self, e: ft.RouteChangeEvent):
        print(f"Route changed to {e.route}")
        self.route = e.route

    async def view_popped(self, e: ft.ViewPopEvent):
        print("View popped")
        views = ft.unwrap_component(ft.context.page.views)
        if len(views) > 1:
            await ft.context.page.push_route(views[-2].route)
