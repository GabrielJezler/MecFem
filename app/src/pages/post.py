import flet as ft

from contexts import ThemeContext

@ft.component
def PostContent():
    theme = ft.use_context(ThemeContext)

    return ft.Container(
        expand=True,
        padding=8,
        border_radius=16,
        bgcolor=theme.colors["bg"],
        content=None
    )