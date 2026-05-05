import flet as ft

import themes
from structures.contexts import ThemeContext, SimulationContext, OrientationContext

from .tooltip import Tooltip

@ft.component
def SimulationStatus() -> ft.Control:
    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)
    orientation = ft.use_context(OrientationContext)

    material_color = ft.Colors.with_opacity(
        1.0 if simulation.state.material else 0., 
        theme.colors["primary"] 
    )
    mesh_color = ft.Colors.with_opacity(
        1.0 if simulation.state.mesh else 0., 
        theme.colors["primary"]
    )
    model_color = ft.Colors.with_opacity(
        1.0 if simulation.state.model else 0., 
        theme.colors["primary"]
    )
    ran_color = ft.Colors.with_opacity(
        1.0 if simulation.state.ran else 0., 
        theme.colors["primary"]
    )

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
                    "Status  " if orientation == ft.Orientation.LANDSCAPE else None,
                    style=themes.text.title_medium(theme.mode, bold=True),
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(
                    bgcolor=material_color,
                    border_radius=8,
                    border=ft.Border.all(2, theme.colors['primary']),
                    padding=4,
                    content=ft.Icon(
                        icon=ft.CupertinoIcons.LAB_FLASK,
                        color=theme.colors['text'],
                        size=icon_size,
                        tooltip=Tooltip(
                            message=simulation.state.material.__repr__() if simulation.state.material else "No material defined"
                        )
                    ),
                ),
                ft.Container(
                    bgcolor=mesh_color,
                    border_radius=8,
                    border=ft.Border.all(2, theme.colors['primary']),
                    padding=4,
                    content=ft.Icon(
                        icon=ft.CupertinoIcons.SQUARE_GRID_4X3_FILL,
                        color=theme.colors['text'],
                        size=icon_size,
                        tooltip=Tooltip(
                            message=simulation.state.mesh.__repr__() if simulation.state.mesh else "No mesh defined"
                        )
                    ),
                ),
                ft.Container(
                    bgcolor=model_color,
                    border_radius=8,
                    border=ft.Border.all(2, theme.colors['primary']),
                    padding=4,
                    content=ft.Icon(
                        icon=ft.CupertinoIcons.DOC_CHART,
                        color=theme.colors['text'],
                        size=icon_size,
                        tooltip=Tooltip(
                            message=simulation.state.model.__repr__() if simulation.state.model else "No model defined"
                        )
                    ),
                ),
                ft.Container(
                    bgcolor=ran_color,
                    border_radius=8,
                    border=ft.Border.all(2, theme.colors['primary']),
                    padding=4,
                    content=ft.Icon(
                        icon=ft.CupertinoIcons.PLAY,
                        color=theme.colors['text'],
                        size=icon_size,
                        tooltip=Tooltip(
                            message="Simulation has been run" if simulation.state.ran else "Simulation has not been run"
                        )
                    ),
                ),
            ]
        )
    )
