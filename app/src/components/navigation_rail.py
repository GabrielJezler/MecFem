import flet as ft
from collections.abc import Callable

from utils import tomltools
import themes
from contexts import ThemeContext
from states import AppState, SimulationState
from page_data import Page

@ft.component
def SimulationStatus(app:AppState):
    COLORS = tomltools.load_colors()

    # Force re-render by watching the simulation_data object itself
    _ = ft.use_state(app.simulation_data)

    # Determine colors based on current state
    material_color = COLORS["ui"][app.theme_mode.value]["success"] if app.simulation_data.material else COLORS["ui"][app.theme_mode.value]["alert"]
    mesh_color = COLORS["ui"][app.theme_mode.value]["success"] if app.simulation_data.mesh else COLORS["ui"][app.theme_mode.value]["alert"]
    model_color = COLORS["ui"][app.theme_mode.value]["success"] if app.simulation_data.model else COLORS["ui"][app.theme_mode.value]["alert"]
    ran_color = COLORS["ui"][app.theme_mode.value]["success"] if app.simulation_data.ran else COLORS["ui"][app.theme_mode.value]["alert"]

    return ft.Container(
        padding=6,
        border_radius=12,
        bgcolor=COLORS["ui"][app.theme_mode.value]["primary"],
        content=ft.Column(
            spacing=8,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.Text(
                    "Status",
                    style=themes.text.theme(app.theme_mode).title_small,
                    color=COLORS["ui"][app.theme_mode.value]["bg"],
                ),
                ft.Row(
                    controls=[
                        ft.Icon(
                            icon=ft.CupertinoIcons.LAB_FLASK,
                            color=material_color,
                            size=20,
                            tooltip=ft.Tooltip(
                                message=app.simulation_data.material.__repr__() if app.simulation_data.material else "No material defined",
                                decoration=ft.BoxDecoration(
                                    bgcolor=COLORS["ui"][app.theme_mode.value]["primary"],
                                    border=ft.Border.all(1, COLORS["ui"][app.theme_mode.value]["text"]),
                                )
                            )
                        ),
                        ft.Icon(
                            icon=ft.CupertinoIcons.SQUARE_GRID_4X3_FILL,
                            color=mesh_color,
                            size=20,
                            tooltip=ft.Tooltip(
                                message=app.simulation_data.mesh.__repr__() if app.simulation_data.mesh else "No mesh defined",
                                decoration=ft.BoxDecoration(
                                    bgcolor=COLORS["ui"][app.theme_mode.value]["primary"],
                                    border=ft.Border.all(1, COLORS["ui"][app.theme_mode.value]["text"]),
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
                                message=app.simulation_data.model.__repr__() if app.simulation_data.model else "No model defined",
                                decoration=ft.BoxDecoration(
                                    bgcolor=COLORS["ui"][app.theme_mode.value]["primary"],
                                    border=ft.Border.all(1, COLORS["ui"][app.theme_mode.value]["text"]),
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
    COLORS = tomltools.load_colors()

    return ft.FloatingActionButton(
        icon=ft.Icon(
            ft.CupertinoIcons.SUN_MAX_FILL if theme.mode == ft.ThemeMode.LIGHT else ft.CupertinoIcons.MOON_FILL,
            color=COLORS["ui"][theme.mode.value]["bg"],
        ),
        bgcolor=COLORS["ui"][theme.mode.value]["primary"],
        shape=ft.RoundedRectangleBorder(radius=12),
        on_click=lambda _: theme.toggle(),
    )

@ft.component
def AppNavigationRail(app, pages:list[Page], selected_index: int, on_change:Callable[[int], None]):
    return ft.NavigationRail(
        selected_index=selected_index,
        on_change=lambda e: on_change(e),
        label_type=ft.NavigationRailLabelType.ALL,
        group_alignment=-1.0,
        leading=SimulationStatus(app=app),
        destinations=[
            ft.NavigationRailDestination(
                selected_icon=ft.Icon(
                    icon=page.icon,
                    color=app.colors["ui"][app.theme_mode.value]["bg"]
                ), 
                icon=ft.Icon(
                    icon=page.icon,
                    color=app.colors["ui"][app.theme_mode.value]["text"]
                ), 
                label=page.name,
                indicator_shape=ft.RoundedRectangleBorder(radius=12)
            ) for page in pages
        ],
        trailing=ThemeButton(),
    )
