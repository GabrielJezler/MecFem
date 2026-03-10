import flet as ft
from dataclasses import dataclass
from collections.abc import Callable

from states import AppState, SimulationState

@dataclass(frozen=True)
class ThemeContextValue:
    mode: ft.ThemeMode
    toggle: Callable[[], None]

ThemeContext = ft.create_context(ThemeContextValue(ft.ThemeMode.LIGHT, lambda: None))

# AppContext = ft.create_context(
#     AppState(
#         route="/",
#         theme_mode=ft.ThemeMode.LIGHT,
#         colors={},
#         config={},
#         simulation_data=SimulationState(),
#     )
# )