import flet as ft
import inspect

from ._base import BasePage
from utils import tomltools

@ft.component
def RunContent(app) -> ft.Control:
    def get_model_params() -> dict[str, dict[str, str | None]]:
        if app.simulation_data.model:
            sig = inspect.signature(app.simulation_data.model.solve)

            params = {}
            for param in sig.parameters:
                if sig.parameters[param].kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                    params[param] = {
                        "type": sig.parameters[param].annotation,
                        "default": sig.parameters[param].default if sig.parameters[param].default is not inspect.Parameter.empty else None
                    }

            return params

        return None
    
    COLORS = tomltools.load_colors()
    
    def number_input(param_name:str, param_info:dict[str, str | None]):
        return ft.TextField(
            label=param_name,
            value=str(param_info["default"]) if param_info["default"] is not None else None,
            border_color=COLORS["ui"][app.theme_mode.value]["primary"],
            input_filter=ft.InputFilter(
                regex_string=r"^[0-9]*\.?[0-9]*$",
                allow=True,
                replacement_string="",
            ),
            col={
                ft.ResponsiveRowBreakpoint.XS: 12,
                ft.ResponsiveRowBreakpoint.MD: 4,
            },
            # on_change=lambda e: update_param_value(param_name, e.control.value),
        )
    
    def bool_input(param_name:str, param_info:dict[str, str | None]):
        return ft.Switch(
            adaptive=True,
            label=param_name,
            value=param_info["default"] if param_info["default"] is not None else False,
            active_color=COLORS["ui"][app.theme_mode.value]["primary"],
            inactive_track_color=COLORS["ui"][app.theme_mode.value]["bg"],
            inactive_thumb_color=COLORS["ui"][app.theme_mode.value]["text"],
            col={
                ft.ResponsiveRowBreakpoint.XS: 12,
                ft.ResponsiveRowBreakpoint.MD: 4,
            },
            # on_change=lambda e: update_param_value(param_name, e.control.value),
        )

    def build_input_controls():
        PARAMS = get_model_params()

        if not PARAMS:
            return ft.Text("No parameters found. Select a material, mesh and model before running the simulation.")

        return ft.ResponsiveRow(
            controls=[
                number_input(param_name, param_info) if param_info["type"] in (int, float) else bool_input(param_name, param_info)
                for param_name, param_info in PARAMS.items()
            ]
        )

    return ft.Container(
        expand=True,
        padding=2,
        content=ft.Column(
            controls=[
                build_input_controls(),
                ft.TextButton(
                    content=ft.Text("Run Simulation"),
                    expand=False,
                    height=48,
                    # on_click=lambda e: show_mesh(e),
                )
            ],
            alignment=ft.MainAxisAlignment.START,
        )
    )

def run(
        app
    ):

    return BasePage(
        app,
        title="Run",
        description="Execute the simulation with the defined parameters",
        primary_content=RunContent(app)
    )