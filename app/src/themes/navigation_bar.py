import flet as ft

from . import text
from utils import tomltools

def theme(theme_mode:ft.ThemeMode) -> ft.NavigationBarTheme:
    COLORS = tomltools.load_colors()
    
    return ft.NavigationBarTheme(
        bgcolor=COLORS[theme_mode.value]["bg"],
        elevation=0,
        label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
        label_text_style=text.body_medium(theme_mode, size=15, color=COLORS[theme_mode.value]["primary"], bold=True),
        indicator_color=COLORS[theme_mode.value]["primary"],
        indicator_shape=ft.RoundedRectangleBorder(radius=12)
    )
