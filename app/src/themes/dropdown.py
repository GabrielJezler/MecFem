import flet as ft

from . import text
from utils import tomltools

def theme(theme_mode:ft.ThemeMode) -> ft.DropdownTheme:
    COLORS = tomltools.load_colors()
    
    return ft.DropdownTheme(
        text_style=text.body_medium(theme_mode, color=COLORS[theme_mode.value]["primary"], bold=True),
    )