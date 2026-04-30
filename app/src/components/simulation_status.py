import flet as ft

import themes
from states import *
from contexts import *

from .tooltip import Tooltip

@ft.component
def SimulationStatus(app:AppState) -> ft.Control:

    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    material_color = theme.colors["success"] if simulation.state.material else theme.colors["danger"]
    mesh_color = theme.colors["success"] if simulation.state.mesh else theme.colors["danger"]
    model_color = theme.colors["success"] if simulation.state.model else theme.colors["danger"]
    ran_color = theme.colors["success"] if simulation.state.ran else theme.colors["danger"]

    icon_size = 20

    return ft.Container(
        padding=8,
        border_radius=16,
        bgcolor=theme.colors["bg_02"],
        content=ft.Row(
            spacing=8,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Status  ",
                    style=themes.text.body_large(theme.mode, bold=True),
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.1, material_color),
                    border_radius=8,
                    border=ft.Border.all(1, material_color),
                    padding=4,
                    content=ft.Icon(
                        icon=ft.CupertinoIcons.LAB_FLASK,
                        color=material_color,
                        size=icon_size,
                        tooltip=Tooltip(
                            message=simulation.state.material.__repr__() if simulation.state.material else "No material defined"
                        )
                    ),
                ),
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.1, mesh_color),
                    border_radius=8,
                    border=ft.Border.all(1, mesh_color),
                    padding=4,
                    content=ft.Icon(
                        icon=ft.CupertinoIcons.SQUARE_GRID_4X3_FILL,
                        color=mesh_color,
                        size=icon_size,
                        tooltip=Tooltip(
                            message=simulation.state.mesh.__repr__() if simulation.state.mesh else "No mesh defined"
                        )
                    ),
                ),
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.1, model_color),
                    border_radius=8,
                    border=ft.Border.all(1, model_color),
                    padding=4,
                    content=ft.Icon(
                        icon=ft.CupertinoIcons.DOC_CHART,
                        color=model_color,
                        size=icon_size,
                        tooltip=Tooltip(
                            message=simulation.state.model.__repr__() if simulation.state.model else "No model defined"
                        )
                    ),
                ),
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.1, ran_color),
                    border_radius=8,
                    border=ft.Border.all(1, ran_color),
                    padding=4,
                    content=ft.Icon(
                        icon=ft.CupertinoIcons.PLAY,
                        color=ran_color,
                        size=icon_size,
                        tooltip=Tooltip(
                            message="Simulation has been run" if simulation.state.ran else "Simulation has not been run"
                        )
                    ),
                ),
            ]
        )
    )
