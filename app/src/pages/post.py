import flet as ft

from ._base import BasePage

def post(
        app
    ):

    return BasePage(
        app,
        title="Post-Processing",
        description="Visualize and analyze simulation results",
        # primary_content=primary_content
    )