import flet as ft

from contexts import ThemeContext

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