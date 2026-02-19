import flet as ft

from ._base import BasePage

def bc(
        app,
    ):

    return BasePage(
        app,
        title="Boundary Conditions",
        description="Define boundary conditions for the simulation",
        # primary_content=primary_content
    )