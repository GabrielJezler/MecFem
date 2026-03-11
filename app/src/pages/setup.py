import flet as ft
import inspect
import pkgutil
import importlib
import asyncio

import MecFEM as mf

from utils import tomltools, stringtools
import themes
from components import BasePage, ErrorDialog
from contexts import *

@ft.component
def SetupContent() -> ft.Control:    
    def model_name_str(name:str | None=None):
        if name:
            return stringtools.pascal_to_string(name)
        return None

    def get_models() -> dict[str, type]:
        models = {}

        for _, module_name, _ in pkgutil.walk_packages(
            mf.models.__path__, mf.models.__name__ + "."
        ):
            if "base" not in module_name.lower().split("."):
                module = importlib.import_module(module_name)

                for name, cls in inspect.getmembers(module, inspect.isclass):
                    if cls.__module__ == module.__name__:
                        models[name] = cls

        return models
    
    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    MODELS = get_models()

    model_name_text, set_model_name_text = ft.use_state(model_name_str())

    model_dropdown_ref = ft.Ref[ft.Dropdown]()

    def save_model(e: ft.ControlEvent) -> None:
        name = e.control.value
        model = MODELS.get(stringtools.string_to_pascal(name))

        simulation.state.model = None
        if model:
            try:
                mesh = simulation.state.mesh
                material = simulation.state.material
                if mesh and material:
                    simulation.state.model = model(mesh=mesh, material=material)
                    set_model_name_text(model_name_str(name))
                else:
                    if mesh is None and material is None:
                        raise AttributeError("Mesh and material must be defined to create the model.")
                    elif mesh is None:
                        raise AttributeError("Mesh must be defined to create the model.")
                    elif material is None:
                        raise AttributeError("Material must be defined to create the model.")
            except Exception as ex:
                ErrorDialog(theme, "Model not saved", f"ERROR: {ex}")
                set_model_name_text(model_name_str())
        else:
            set_model_name_text(model_name_str())
            ErrorDialog(theme, "No model selected", "Please select a model before saving.")

    def mount():
        if simulation.state.model:
            set_model_name_text(model_name_str(simulation.state.model.__class__.__name__))

    ft.use_effect(mount, [])

    return ft.Container(
        expand=True,
        padding=2,
        content=ft.Column(
            controls=[
                ft.Dropdown(
                    ref=model_dropdown_ref,
                    value=model_name_text,
                    label="Select Model",
                    label_style=themes.text.body_medium(theme.mode),
                    border_color=theme.colors["primary"],
                    options=[
                        ft.DropdownOption(
                            text=model_name_str(name)
                        )
                        for name in MODELS.keys()
                    ],
                    col={
                        ft.ResponsiveRowBreakpoint.XS: 12,
                        ft.ResponsiveRowBreakpoint.MD: 6,
                    },
                    on_select=lambda e: save_model(e),
                    expand=True
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )

def setup():
    return BasePage(
        title="Model",
        primary_content=SetupContent()
    )