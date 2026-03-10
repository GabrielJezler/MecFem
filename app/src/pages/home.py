import flet as ft

from components import BasePage

@ft.component
def home(
        app
    ):

    return BasePage(
        app,
        title="Home",
        description="Welcome to the MecFEM application.",
        # primary_content=
    )