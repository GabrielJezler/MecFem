import flet as ft
from typing import Any

from themes import text
from utils import tomltools

@ft.component
def BasePage(
            app,
            title: str = "Base Page",
            description: str = "This is the base page for the application.",
            primary_content: ft.Control = ft.Text("No content provided."),
        ):

        COLORS = tomltools.load_colors()

        return ft.Container(
            padding = ft.Padding.only(left=6, right=2, top=2, bottom=2),
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text(
                        title, 
                        style=text.title_large(app.theme_mode)
                    ),
                    ft.Divider(
                        height=4.,
                        thickness=4., 
                        color=COLORS["ui"][app.theme_mode.value]["primary"],
                        radius=2,
                    ),
                    ft.Text(
                        description, 
                        style=text.body_medium(app.theme_mode, italic=True),
                    ),
                    primary_content
                ],
                spacing=12,
            )
        )
