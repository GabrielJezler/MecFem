import flet as ft

from . import text
from utils import tomltools

def theme(theme_mode:ft.ThemeMode) -> ft.TextButtonTheme:
    COLORS = tomltools.load_colors()
    
    return ft.TextButtonTheme(
        style=ft.ButtonStyle(
            color=COLORS[theme_mode.value]["bg"],
            bgcolor=COLORS[theme_mode.value]["primary"],
            shape=ft.RoundedRectangleBorder(radius=4),
            padding=ft.Padding(16, 12, 16, 12),
            text_style=text.body_large(theme_mode, bold=True),
        )
    )