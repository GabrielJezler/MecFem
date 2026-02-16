import flet as ft
import toml

from utils import tomltools

def body_small(page:ft.Page, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=False, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()
    return ft.TextStyle(
        font_family=CONFIG["fonts"]["body"] if font_family is None else font_family,
        size=12 if size is None else size,
        color=COLORS["ui"][page.theme_mode.value]["text"],
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def body_medium(page:ft.Page, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=False, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()

    return ft.TextStyle(
        font_family=CONFIG["fonts"]["body"] if font_family is None else font_family,
        size=16 if size is None else size,
        color=COLORS["ui"][page.theme_mode.value]["text"] if color is None else color,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def body_large(page:ft.Page, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=False, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()

    return ft.TextStyle(
        font_family=CONFIG["fonts"]["body"] if font_family is None else font_family,
        size=20 if size is None else size,
        color=COLORS["ui"][page.theme_mode.value]["text"] if color is None else color,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def title_small(page:ft.Page, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=True, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()

    return ft.TextStyle(
        font_family=CONFIG["fonts"]["title"] if font_family is None else font_family,
        size=18 if size is None else size,
        color=COLORS["ui"][page.theme_mode.value]["text"] if color is None else color,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def title_medium(page:ft.Page, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=True, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()

    return ft.TextStyle(
        font_family=CONFIG["fonts"]["title"] if font_family is None else font_family,
        size=22 if size is None else size,
        color=COLORS["ui"][page.theme_mode.value]["text"] if color is None else color,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def title_large(page:ft.Page, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=True, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()

    return ft.TextStyle(
        font_family=CONFIG["fonts"]["title"] if font_family is None else font_family,
        size=26 if size is None else size,
        color=COLORS["ui"][page.theme_mode.value]["text"] if color is None else color,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def theme(page:ft.Page):
    return ft.TextTheme(
            body_small=body_small(page),
            body_medium=body_medium(page),
            body_large=body_large(page),
            title_small=title_small(page),
            title_medium=title_medium(page),
            title_large=title_large(page),
        )