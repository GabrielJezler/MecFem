import flet as ft

from ._base import BasePage

def home(
        page:ft.Page,
        title: str | None=None,
        description: str | None=None,
    ):

    return BasePage(
        page=page,
        title=title if title else "Home",
        description=description if description else "Welcome to the home page of the application.",
        # primary_content=primary_content
    )