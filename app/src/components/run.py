import flet as ft

from ._base import BasePage

def run(
        app
    ):

    return BasePage(
        app,
        title="Run",
        description="Execute the simulation with the defined parameters",
    )