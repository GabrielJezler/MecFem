import flet as ft

from states import *
from contexts import *

from .simulation_status import SimulationStatus
from .buttons import LoadSimulationButton, SaveSimulationButton, ThemeButton

@ft.component
def AppBar(app: AppState) -> ft.Control:
    theme = ft.use_context(ThemeContext)

    return ft.Container(
        content=ft.Row(
            controls=[
                SimulationStatus(app),
                ft.Row(
                    spacing=8,
                    controls=[
                        LoadSimulationButton(),
                        SaveSimulationButton(),
                        ThemeButton(),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            margin=0,
        ),
        padding=0,
    )