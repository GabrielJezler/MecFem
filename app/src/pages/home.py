import flet as ft

from contexts import ThemeContext
from components import Panel

@ft.component
def HomeContent() -> ft.Control:
    theme = ft.use_context(ThemeContext)

    return ft.Container(
        expand=True,
        padding=8,
        border_radius=16,
        bgcolor=theme.colors["bg"],
        content=None
    )