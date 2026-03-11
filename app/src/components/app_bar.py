import flet as ft

from states import *
from contexts import *

from .simulation_status import HorizontalSimulationStatus
from .theme_button import ThemeButton

@ft.component
def AppBar(app: AppState) -> ft.Control:
    theme = ft.use_context(ThemeContext)

    return ft.AppBar(
        leading=HorizontalSimulationStatus(app),
        leading_width=240,
        title=None,
        actions=ThemeButton(),
        actions_padding=8,
        bgcolor=theme.colors["bg"],
    )
