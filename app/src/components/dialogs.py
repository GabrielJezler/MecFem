import flet as ft

import themes
from contexts import *

# @ft.component
def ErrorDialog(theme:ThemeContextValue, title:str, text:str):
    # theme = ft.use_context(ThemeContext)
    
    dialog = ft.AlertDialog(
        title=ft.Text(
            title, 
            style=themes.text.title_medium(theme.mode, color=theme.colors["primary"])
        ),
        content=ft.Text(
            text, 
            style=themes.text.body_medium(theme.mode)
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