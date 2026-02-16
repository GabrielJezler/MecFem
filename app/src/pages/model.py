import flet as ft

from ._base import BasePage

def model(
        page:ft.Page,
        title: str | None=None,
        description: str | None=None,
    ):

    return BasePage(
        page=page,
        title=title,
        description=description,
        # primary_content=primary_content
    )