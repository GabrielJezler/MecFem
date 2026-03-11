import flet as ft
from collections.abc import Callable
import asyncio

from utils import tomltools
import themes
from contexts import *
from states import AppState, SimulationState

from .simulation_status import VerticalSimulationStatus
from .theme_button import ThemeButton

@ft.component
def AppNavigationRail(app:AppState) -> ft.Control:
    def navigate(e: ft.ControlEvent):
        route = app.pages[e.control.selected_index].route
        if route != app.route:
            asyncio.create_task(ft.context.page.push_route(route))

    theme = ft.use_context(ThemeContext)

    return ft.NavigationRail(
        selected_index=app.get_page_index(),
        on_change=lambda e: navigate(e),
        label_type=ft.NavigationRailLabelType.ALL,
        group_alignment=-1.0,
        extended=False,
        destinations=[
            ft.NavigationRailDestination(
                selected_icon=ft.Icon(
                    icon=page.icon,
                    color=theme.colors["bg"]
                ), 
                icon=ft.Icon(
                    icon=page.icon,
                    color=theme.colors["text"]
                ), 
                label=page.name,
                indicator_shape=ft.RoundedRectangleBorder(radius=12)
            ) for page in app.pages
        ],
    )
