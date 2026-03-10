import flet as ft
import inspect
import pkgutil
import importlib
import asyncio

import MecFEM as mf

from utils import tomltools, stringtools
import themes
from components import BasePage, ErrorDialog

@ft.component
def SetupContent(app) -> ft.Control:    
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

    COLORS = tomltools.load_colors()
    MODELS = get_models()
    model_name_text, set_model_name_text = ft.use_state(model_name_str())

    model_dropdown_ref = ft.Ref[ft.Dropdown]()

    def save_model(e: ft.ControlEvent) -> None:
        name = e.control.value
        model = MODELS.get(stringtools.string_to_pascal(name))

        app.simulation_data.model = None
        if model:
            try:
                mesh = app.simulation_data.mesh
                material = app.simulation_data.material
                if mesh and material:
                    app.simulation_data.model = model(mesh=mesh, material=material)
                else:
                    if mesh is None and material is None:
                        raise ValueError("Mesh and material must be defined to create the model.")
                    elif mesh is None:
                        raise ValueError("Mesh must be defined to create the model.")
                    elif material is None:
                        raise ValueError("Material must be defined to create the model.")
            except Exception as ex:
                ErrorDialog(app, "Model not saved", f"ERROR: {ex}")
                set_model_name_text(model_name_str())
        else:
            set_model_name_text(model_name_str())
            ErrorDialog(app, "No model selected", "Please select a model before saving.")

    def mount():
        if app.simulation_data.model:
            set_model_name_text(model_name_str(app.simulation_data.model.__class__.__name__))

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
                    label_style=themes.text.body_medium(app.theme_mode),
                    border_color=COLORS["ui"][app.theme_mode.value]["primary"],
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

def setup(
        app,
    ):

    return BasePage(
        app,
        title="Model",
        description="Define the model for the simulation",
        primary_content=SetupContent(app)
    )