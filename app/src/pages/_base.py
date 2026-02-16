import flet as ft
from typing import Any

from themes import text
from utils import tomltools

class BasePage(ft.Container):
    def __init__(
            self, 
            page: ft.Page,
            title: str = "Base Page",
            description: str = "This is the base page for the application.",
            primary_content: ft.Control = ft.Text("No content provided."),
            data: Any = None
        ):
        super().__init__()

        COLORS = tomltools.load_colors()

        self.data = data

        self.padding = ft.Padding.only(left=6, right=2, top=2, bottom=2)
        self.expand = True

        self.primary_content = primary_content

        self.content = ft.Column(
            controls=[
                ft.Text(
                    title, 
                    style=text.title_large(page)
                ),
                ft.Divider(
                    height=4.,
                    thickness=4., 
                    color=COLORS["ui"][page.theme_mode.value]["primary"],
                    radius=2,
                ),
                ft.Text(
                    description, 
                    style=text.body_medium(page, italic=True),
                ),
                self.primary_content
            ],
            spacing=12,
        )

