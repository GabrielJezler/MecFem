import flet as ft
from collections.abc import Callable
import asyncio

from utils import tomltools
import themes
from contexts import *
from states import AppState, SimulationState

@ft.component
def SimulationStatus(app:AppState) -> ft.Control:
    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    # Determine colors based on current state
    material_color = theme.colors["success"] if simulation.state.material else theme.colors["alert"]
    mesh_color = theme.colors["success"] if simulation.state.mesh else theme.colors["alert"]
    model_color = theme.colors["success"] if simulation.state.model else theme.colors["alert"]
    ran_color = theme.colors["success"] if simulation.state.ran else theme.colors["alert"]

    return ft.Container(
        padding=6,
        border_radius=12,
        bgcolor=theme.colors["primary"],
        content=ft.Column(
            spacing=8,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.Text(
                    "Status",
                    style=themes.text.theme(app.theme_mode).title_small,
                    color=theme.colors["bg"],
                ),
                ft.Row(
                    controls=[
                        ft.Icon(
                            icon=ft.CupertinoIcons.LAB_FLASK,
                            color=material_color,
                            size=20,
                            tooltip=ft.Tooltip(
                                message=simulation.state.material.__repr__() if simulation.state.material else "No material defined",
                                decoration=ft.BoxDecoration(
                                    bgcolor=theme.colors["primary"],
                                    border=ft.Border.all(1, theme.colors["text"]),
                                )
                            )
                        ),
                        ft.Icon(
                            icon=ft.CupertinoIcons.SQUARE_GRID_4X3_FILL,
                            color=mesh_color,
                            size=20,
                            tooltip=ft.Tooltip(
                                message=simulation.state.mesh.__repr__() if simulation.state.mesh else "No mesh defined",
                                decoration=ft.BoxDecoration(
                                    bgcolor=theme.colors["primary"],
                                    border=ft.Border.all(1, theme.colors["text"]),
                                )
                            )
                        ),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                ft.Row(
                    controls=[
                        ft.Icon(
                            icon=ft.CupertinoIcons.DOC_CHART,
                            color=model_color,
                            size=20,
                            tooltip=ft.Tooltip(
                                message=simulation.state.model.__repr__() if simulation.state.model else "No model defined",
                                decoration=ft.BoxDecoration(
                                    bgcolor=theme.colors["primary"],
                                    border=ft.Border.all(1, theme.colors["text"]),
                                )
                            )
                        ),
                        ft.Icon(
                            icon=ft.CupertinoIcons.PLAY,
                            color=ran_color,
                            size=20,
                        ),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                )
            ]
        )
    )

@ft.component
def ThemeButton():
    theme = ft.use_context(ThemeContext)

    return ft.FloatingActionButton(
        icon=ft.Icon(
            ft.CupertinoIcons.SUN_MAX_FILL if theme.mode == ft.ThemeMode.LIGHT else ft.CupertinoIcons.MOON_FILL,
            color=theme.colors["bg"],
        ),
        bgcolor=theme.colors["primary"],
        shape=ft.RoundedRectangleBorder(radius=12),
        on_click=lambda _: theme.toggle(),
    )

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
        leading=SimulationStatus(app=app),
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
        trailing=ThemeButton(),
    )
