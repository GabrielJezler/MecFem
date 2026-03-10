import flet as ft

import themes
import utils

def ErrorDialog(app, title:str, text:str):
    COLORS = utils.tomltools.load_colors()
    
    dialog = ft.AlertDialog(
        title=ft.Text(
            title, 
            style=themes.text.title_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["primary"])
        ),
        content=ft.Text(
            text, 
            style=themes.text.body_medium(app.theme_mode)
        ),
        actions=[
            ft.TextButton(
                "Dismiss",
                on_click=lambda e: ft.context.page.pop_dialog(),
                autofocus=True
            )
        ],
        modal=True,
    )
    ft.context.page.show_dialog(dialog)