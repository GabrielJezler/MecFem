import flet as ft

from . import text
from utils import tomltools

def theme(theme_mode:ft.ThemeMode) -> ft.TextButtonTheme:
    COLORS = tomltools.load_colors()
    
    return ft.TextButtonTheme(
        style=ft.ButtonStyle(
            color=COLORS[theme_mode.value]["text"],
            bgcolor=COLORS[theme_mode.value]["bg_01"],
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=12,
            text_style=text.body_medium(theme_mode, bold=True),
        )
    )