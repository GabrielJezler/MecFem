import flet as ft
import toml

from utils import tomltools

def body_small(theme_mode:ft.ThemeMode, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=False, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()
    return ft.TextStyle(
        font_family=CONFIG["fonts"]["body"] if font_family is None else font_family,
        size=12 if size is None else size,
        color=COLORS["ui"][theme_mode.value]["text"] if color is None else color,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def body_medium(theme_mode:ft.ThemeMode, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=False, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()

    return ft.TextStyle(
        font_family=CONFIG["fonts"]["body"] if font_family is None else font_family,
        size=16 if size is None else size,
        color=COLORS["ui"][theme_mode.value]["text"] if color is None else color,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def body_large(theme_mode:ft.ThemeMode, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=False, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()

    return ft.TextStyle(
        font_family=CONFIG["fonts"]["body"] if font_family is None else font_family,
        size=20 if size is None else size,
        color=COLORS["ui"][theme_mode.value]["text"] if color is None else color,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def title_small(theme_mode:ft.ThemeMode, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=True, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()

    return ft.TextStyle(
        font_family=CONFIG["fonts"]["title"] if font_family is None else font_family,
        size=18 if size is None else size,
        color=COLORS["ui"][theme_mode.value]["text"] if color is None else color,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def title_medium(theme_mode:ft.ThemeMode, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=True, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()

    return ft.TextStyle(
        font_family=CONFIG["fonts"]["title"] if font_family is None else font_family,
        size=22 if size is None else size,
        color=COLORS["ui"][theme_mode.value]["text"] if color is None else color,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def title_large(theme_mode:ft.ThemeMode, font_family:str | None=None, size:float | None=None, color:str | None=None, bold:bool=True, italic:bool=False):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()

    return ft.TextStyle(
        font_family=CONFIG["fonts"]["title"] if font_family is None else font_family,
        size=26 if size is None else size,
        color=COLORS["ui"][theme_mode.value]["text"] if color is None else color,
        weight=ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL,
        italic=italic,
    )

def theme(theme_mode:ft.ThemeMode) -> ft.TextTheme:
    return ft.TextTheme(
            body_small=body_small(theme_mode),
            body_medium=body_medium(theme_mode),
            body_large=body_large(theme_mode),
            title_small=title_small(theme_mode),
            title_medium=title_medium(theme_mode),
            title_large=title_large(theme_mode),
        )