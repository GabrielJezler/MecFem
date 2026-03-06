import flet as ft

from . import text
from utils import tomltools

def theme(theme_mode:ft.ThemeMode) -> ft.TooltipTheme:
    COLORS = tomltools.load_colors()
    
    return ft.TooltipTheme(
        text_style=text.body_medium(theme_mode, color=COLORS["ui"][theme_mode.value]["text"]),
    )