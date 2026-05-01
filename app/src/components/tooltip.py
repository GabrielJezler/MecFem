import flet as ft

from structures.contexts import ThemeContext

@ft.component
def Tooltip(message:str, wait_duration:ft.DurationValue | None = None) -> ft.Control:
    theme = ft.use_context(ThemeContext)

    return ft.Tooltip(
        message=message,
        wait_duration=wait_duration if wait_duration else None,
        decoration=ft.BoxDecoration(
            bgcolor=theme.colors["bg_02"],
            border=ft.Border.all(2, theme.colors["bg"]),
            border_radius=8,
        )
    )
