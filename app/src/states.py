import flet as ft
import asyncio
from dataclasses import dataclass, field
from typing import Any
from collections.abc import Callable

import MecFEM as mf

from utils import tomltools

@ft.observable
@dataclass
class SimulationState:
    material: Any = None
    mesh: mf.mesh.Mesh | None = None
    model: mf.models.Linear | mf.models.NonLinear | None = None
    ran: bool = False

    def __repr__(self):
        return f"SimulationState(material={self.material}, mesh={self.mesh}, model={self.model.__class__.__name__}, ran={self.ran})"


@ft.observable
@dataclass
class PageState:
    name: str
    route: str
    index:int
    icon: ft.Icon
    content_function: Callable[[], ft.Control]

    def build(self) -> ft.Control:
        return self.content_function()


@ft.observable
@dataclass
class AppState:
    route: str
    theme_mode: ft.ThemeMode
    config: dict
    pages: list[PageState] = field(default_factory=list)

    def toggle_theme(self):
        self.theme_mode = (
            ft.ThemeMode.DARK
            if self.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        
        self.config["theme"]["mode"] = "dark" if self.theme_mode == ft.ThemeMode.DARK else "light"
        tomltools.update_config(self.config)

    def route_change(self, e: ft.RouteChangeEvent):
        self.route = e.route

    async def view_popped(self, e: ft.ViewPopEvent):
        print("View popped")
        views = ft.unwrap_component(ft.context.page.views)
        if len(views) > 1:
            await ft.context.page.push_route(views[-2].route)

    def get_page_index(self) -> int:
        routes = [page.route for page in self.pages]
        if self.route in routes:
            return routes.index(self.route)
        else :
            return routes.index("/")

    def get_page(self) -> PageState:
        index = self.get_page_index()
        return self.pages[index]

    def build_page(self) -> ft.Control:
        page = self.get_page()
        return page.build()