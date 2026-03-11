import flet as ft

from components import BasePage
from contexts import ThemeContext, SimulationContext

@ft.component
def HomeContent() -> ft.Control:
    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    return ft.Text(
        f"Hello, \ntheme: {theme.mode.value}\ncolors: {theme.colors}\nconfig: {theme.config} \nsimulation: {simulation.state}", 
    )


@ft.component
def home():
    return BasePage(
        title="Home",
        description="Welcome to the MecFEM application.",
        primary_content=HomeContent()
    )