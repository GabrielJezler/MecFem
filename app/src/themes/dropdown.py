import flet as ft

from . import text
from utils import tomltools

def theme(page:ft.Page):
    COLORS = tomltools.load_colors()
    
    return ft.DropdownTheme(
        text_style=text.body_medium(page, color=COLORS["ui"][page.theme_mode.value]["primary"], bold=True),
    )