import flet as ft

from ._base import BasePage

@ft.component
def home(
        app
    ):

    return BasePage(
        app,
        title="Home",
        description="Welcome to the MecFEM application.",
        # primary_content=primary_content
    )