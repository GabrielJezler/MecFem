import flet as ft

from components import BasePage, ErrorDialog

def post(
        app
    ):

    return BasePage(
        app,
        title="Post-Processing",
        description="Visualize and analyze simulation results",
        # primary_content=primary_content
    )