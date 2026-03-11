import flet as ft

import themes
from states import *
from contexts import *

@ft.component
def VerticalSimulationStatus(app:AppState) -> ft.Control:
    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    # Determine colors based on current state
    material_color = theme.colors["success"] if simulation.state.material else theme.colors["alert"]
    mesh_color = theme.colors["success"] if simulation.state.mesh else theme.colors["alert"]
    model_color = theme.colors["success"] if simulation.state.model else theme.colors["alert"]
    ran_color = theme.colors["success"] if simulation.state.ran else theme.colors["alert"]

    icon_size = 25

    return ft.Container(
        padding=6,
        border_radius=12,
        # bgcolor=theme.colors["primary"],
        border=ft.Border.all(1, theme.colors["primary"]),
        content=ft.Column(
            spacing=8,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Status",
                    style=themes.text.theme(app.theme_mode).title_small,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Row(
                    controls=[
                        ft.Icon(
                            icon=ft.CupertinoIcons.LAB_FLASK,
                            color=material_color,
                            size=icon_size,
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
                            size=icon_size,
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
                            size=icon_size,
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
                            size=icon_size,
                        ),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                )
            ]
        )
    )

@ft.component
def HorizontalSimulationStatus(app:AppState) -> ft.Control:
    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    material_color = theme.colors["success"] if simulation.state.material else theme.colors["alert"]
    mesh_color = theme.colors["success"] if simulation.state.mesh else theme.colors["alert"]
    model_color = theme.colors["success"] if simulation.state.model else theme.colors["alert"]
    ran_color = theme.colors["success"] if simulation.state.ran else theme.colors["alert"]

    icon_size = 25

    return ft.Container(
        padding=6,
        margin=8,
        border_radius=12,
        expand=True,
        # bgcolor=theme.colors["primary"],
        border=ft.Border.all(1, theme.colors["primary"]),
        content=ft.Row(
            spacing=8,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Status  ",
                    style=themes.text.theme(app.theme_mode).title_small,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Icon(
                    icon=ft.CupertinoIcons.LAB_FLASK,
                    color=material_color,
                    size=icon_size,
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
                    size=icon_size,
                    tooltip=ft.Tooltip(
                        message=simulation.state.mesh.__repr__() if simulation.state.mesh else "No mesh defined",
                        decoration=ft.BoxDecoration(
                            bgcolor=theme.colors["primary"],
                            border=ft.Border.all(1, theme.colors["text"]),
                        )
                    )
                ),
                ft.Icon(
                    icon=ft.CupertinoIcons.DOC_CHART,
                    color=model_color,
                    size=icon_size,
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
                    size=icon_size,
                ),
            ]
        )
    )
