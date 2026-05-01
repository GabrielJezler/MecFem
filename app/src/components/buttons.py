import flet as ft

from structures.contexts import ThemeContext

from .tooltip import Tooltip

@ft.component
def SaveSimulationButton():
    theme = ft.use_context(ThemeContext)

    return ft.FloatingActionButton(
        icon=ft.Icon(
            ft.CupertinoIcons.ARROW_DOWN_DOC,
            color=theme.colors["text"],
        ),
        bgcolor=theme.colors["bg_02"],
        margin=0,
        mini=True,
        shape=ft.RoundedRectangleBorder(radius=16),
        # on_click=lambda _: theme.toggle(),
        tooltip=Tooltip(
            message="Save simulation to file",
        ),
    )

@ft.component
def LoadSimulationButton():
    theme = ft.use_context(ThemeContext)

    return ft.FloatingActionButton(
        icon=ft.Icon(
            ft.CupertinoIcons.ARROW_UP_DOC,
            color=theme.colors["text"],
        ),
        bgcolor=theme.colors["bg_02"],
        margin=0,
        mini=True,
        shape=ft.RoundedRectangleBorder(radius=16),
        # on_click=lambda _: theme.toggle(), # Add load simulation function
        tooltip=Tooltip(
            message="Load simulation from file",
        ),
    )

@ft.component
def ThemeButton():
    theme = ft.use_context(ThemeContext)

    return ft.FloatingActionButton(
        icon=ft.Icon(
            ft.CupertinoIcons.SUN_MAX_FILL if theme.mode == ft.ThemeMode.LIGHT else ft.CupertinoIcons.MOON_FILL,
            color=theme.colors["text"],
        ),
        bgcolor=theme.colors["bg_02"],
        margin=0,
        mini=True,
        shape=ft.RoundedRectangleBorder(radius=16),
        on_click=lambda _: theme.toggle(),
        tooltip=Tooltip(
            message="Toggle theme",
        ),
    )
