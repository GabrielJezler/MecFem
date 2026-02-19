import flet as ft

from ._base import BasePage

def model(
        app,
    ):

    return BasePage(
        app,
        title="Model",
        description="Define the model for the simulation",
        # primary_content=primary_content
    )