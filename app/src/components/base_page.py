import flet as ft
from typing import Any

from themes import text
from utils import tomltools
from contexts import *

@ft.component
def BasePage(
            title: str = "Base Page",
            description: str = "This is the base page for the application.",
            primary_content: ft.Control = ft.Text("No content provided."),
        ):

        theme = ft.use_context(ThemeContext)

        return ft.Container(
            padding = ft.Padding.only(left=6, right=2, top=2, bottom=2),
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text(
                        title, 
                        style=text.title_large(theme.mode)
                    ),
                    ft.Divider(
                        height=4.,
                        thickness=4., 
                        color=theme.colors["primary"],
                        radius=2,
                    ),
                    ft.Text(
                        description, 
                        style=text.body_medium(theme.mode, italic=True),
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                primary_content
                            ],
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                            margin=0,
                        ),
                        expand=True,
                        margin=0,
                        padding=0,
                    )
                ],
                spacing=12,
            )
        )
