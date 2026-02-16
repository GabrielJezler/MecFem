import flet as ft

from . import text
from utils import tomltools

def theme(page:ft.Page):
    COLORS = tomltools.load_colors()
    
    return ft.NavigationRailTheme(
        bgcolor=COLORS["ui"][page.theme_mode.value]["bg"],
        elevation=0,
        unselected_label_text_style=text.body_medium(page),
        selected_label_text_style=text.body_large(page, color=COLORS["ui"][page.theme_mode.value]["primary"], bold=True),
        group_alignment=-1.0,
        indicator_color=COLORS["ui"][page.theme_mode.value]["primary"],
        indicator_shape=ft.RoundedRectangleBorder(radius=12)
    )