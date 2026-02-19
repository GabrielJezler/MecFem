import flet as ft

from . import text
from utils import tomltools

def theme(theme_mode:ft.ThemeMode) -> ft.DialogTheme:
    COLORS = tomltools.load_colors()
    
    return ft.DialogTheme(
        title_text_style=text.title_medium(theme_mode, color=COLORS["ui"][theme_mode.value]["primary"]),
        content_text_style=text.body_medium(theme_mode),
    )