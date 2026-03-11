import flet as ft

from . import text
from utils import tomltools

def theme(theme_mode:ft.ThemeMode) -> ft.NavigationRailTheme:
    COLORS = tomltools.load_colors()
    
    return ft.NavigationRailTheme(
        bgcolor=COLORS[theme_mode.value]["bg"],
        elevation=0,
        min_width=100,
        min_extended_width=100,
        unselected_label_text_style=text.body_medium(theme_mode),
        selected_label_text_style=text.body_large(theme_mode, color=COLORS[theme_mode.value]["primary"], bold=True),
        group_alignment=-1.0,
        indicator_color=COLORS[theme_mode.value]["primary"],
        indicator_shape=ft.RoundedRectangleBorder(radius=12)
    )