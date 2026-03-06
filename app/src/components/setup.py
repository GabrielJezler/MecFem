import flet as ft
import inspect
import pkgutil
import importlib
import asyncio

import MecFEM as mf

from utils import tomltools, stringtools
import themes
from ._base import BasePage

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

    def error_dialog(title:str, text:str):
        dialog = ft.AlertDialog(
            title=ft.Text(
                title, 
                style=themes.text.title_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["primary"])
            ),
            content=ft.Text(
                text, 
                style=themes.text.body_medium(app.theme_mode)
            ),
            actions=[
                ft.TextButton(
                    "Dismiss",
                    on_click=lambda e: ft.context.page.pop_dialog(),
                    autofocus=True
                )
            ],
            modal=True,
        )
        ft.context.page.show_dialog(dialog)

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

                    set_model_name_text(model_name_str(name))
                else:
                    if mesh is None and material is None:
                        raise ValueError("Mesh and material must be defined to create the model.")
                    elif mesh is None:
                        raise ValueError("Mesh must be defined to create the model.")
                    elif material is None:
                        raise ValueError("Material must be defined to create the model.")
            except Exception as ex:
                set_model_name_text(model_name_str())
                error_dialog("Model not saved", f"Error details: {ex}")
        else:
            set_model_name_text(model_name_str())
            error_dialog("No model selected", "Please select a model before saving.")

    def update_from_mesh_material():
        print("--- Update_from_mesh_material called")
        if app.simulation_data.model:
            if app.simulation_data.mesh and app.simulation_data.material:
                try:
                    print("Updating model with new mesh and material...")
                    app.simulation_data.model = app.simulation_data.model.__class__(
                        mesh=app.simulation_data.mesh,
                        material=app.simulation_data.material
                    )
                    print("Model updated with new mesh and material.")
                except Exception as ex:
                    print(f"Error updating model with new mesh and material: {ex}")
            else:
                app.simulation_data.model = None
                print("Mesh or material not defined. Model reset to None.")
        else:
            print("Modelnot defined. Cannot update model.")
    
    # ft.use_effect(
    #     update_from_mesh_material, 
    #     [app.simulation_data]
    # )

    def mount():
        if app.simulation_data.model:
            set_model_name_text(model_name_str(app.simulation_data.model.__class__.__name__))

    ft.use_effect(mount, [])

    return ft.Container(
        expand = True,
        padding = 2,
        content = ft.Column(
            controls=[
                ft.Dropdown(
                    ref=model_dropdown_ref,
                    value=model_name_text,
                    label="Select Model",
                    label_style=themes.text.body_medium(app.theme_mode),
                    border_color=COLORS["ui"][app.theme_mode.value]["primary"],
                    options=[
                        ft.DropdownOption(
                            text=model_name_str(name) # model name converted to display string as text
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