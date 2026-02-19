import flet as ft

from . import text
from utils import tomltools

def theme(theme_mode:ft.ThemeMode) -> ft.ButtonTheme:
    COLORS = tomltools.load_colors()
    
    return ft.ButtonTheme(
        style=ft.ButtonStyle(
            color=COLORS["ui"][theme_mode.value]["text"],
            bgcolor=COLORS["ui"][theme_mode.value]["primary"],
            shape=ft.RoundedRectangleBorder(radius=4),
            padding=ft.Padding(16, 8, 16, 8),
            text_style=text.body_medium(theme_mode, bold=True),
        )
    )