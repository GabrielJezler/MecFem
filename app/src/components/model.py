import flet as ft
import inspect
import pkgutil
import importlib
import asyncio

import MecFEM as mf

from utils import tomltools, stringtools
from themes import text
from ._base import BasePage

@ft.component
def ModelContent(app) -> ft.Control:
    def model_status_str(saved:bool=True):
        if saved:
            return "Model saved successfully."
        return "No model saved."
    
    def model_status_color_str(saved:bool=True):
        if saved:
            return COLORS["ui"][app.theme_mode.value]["success"]
        return COLORS["ui"][app.theme_mode.value]["alert"]
    
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
    models = get_models()

    model_name_text, set_model_name_text = ft.use_state(model_name_str())
    model_status_text, set_model_status_text = ft.use_state(model_status_str(False))
    model_status_color_text, set_model_status_color_text = ft.use_state(model_status_color_str(False))

    model_dropdown_ref = ft.Ref[ft.Dropdown]()

    def no_model_dialog():
        dialog = ft.AlertDialog(
            title=ft.Text(
                "No model selected", 
                style=text.title_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["primary"])
            ),
            content=ft.Text(
                "Please select a model before saving.", 
                style=text.body_medium(app.theme_mode)
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

    def model_not_saved_dialog(exception: Exception = None):
        dialog = ft.AlertDialog(
            title=ft.Text(
                "Model not saved", 
                style=text.title_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["primary"])
            ),
            content=ft.Text(
                value=f"Error details: {exception}",
                style=text.body_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["alert"], italic=True),
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
        model = models.get(name)

        app.simulation_data.model = None

        if model:
            try:
                mesh = app.simulation_data.mesh
                material = app.simulation_data.material
                if mesh and material:
                    app.simulation_data.model = model(mesh=mesh, material=material)

                    set_model_name_text(model_name_str(name))
                    set_model_status_text(model_status_str(True))
                    set_model_status_color_text(model_status_color_str(True))
                    print("Model saved successfully.")
                else:
                    if mesh is None and material is None:
                        raise ValueError("Mesh and material must be defined to create the model.")
                    elif mesh is None:
                        raise ValueError("Mesh must be defined to create the model.")
                    elif material is None:
                        raise ValueError("Material must be defined to create the model.")
            except Exception as ex:
                set_model_name_text(model_name_str())
                set_model_status_text(model_status_str(False))
                set_model_status_color_text(model_status_color_str(False))
                model_not_saved_dialog(ex)
        else:
            set_model_name_text(model_name_str())
            set_model_status_text(model_status_str(False))
            set_model_status_color_text(model_status_color_str(False))
            no_model_dialog()

    def test():
        print(f"--New mesh ref value: {model_dropdown_ref.current.text}")
        print(f"Model: {app.simulation_data.model}")
        print(f"Mesh: {app.simulation_data.mesh}")
        print(f"Material: {app.simulation_data.material}")

    ft.use_effect(test, [model_dropdown_ref])

    def update_from_mesh_material():
        print("update_from_mesh_material called")
        if app.simulation_data.model and app.simulation_data.mesh and app.simulation_data.material:
            try:
                print("Updating model with new mesh and material...")
                app.simulation_data.model = app.simulation_data.model.__class__(
                    mesh=app.simulation_data.mesh,
                    material=app.simulation_data.material
                )
                print("Model updated with new mesh and material.")
            except Exception as ex:
                print(f"Error updating model with new mesh and material: {ex}")
    
    ft.use_effect(
        update_from_mesh_material, 
        [app.simulation_data]
    )

    def mount():
        if app.simulation_data.model:
            set_model_status_text(model_status_str(True))
            set_model_status_color_text(model_status_color_str(True))
            set_model_name_text(model_name_str(app.simulation_data.model.__class__.__name__))

    ft.on_mounted(mount)

    return ft.Container(
        expand = True,
        padding = 2,
        content = ft.Column(
            controls=[
                ft.ResponsiveRow(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Dropdown(
                            ref=model_dropdown_ref,
                            text=model_name_text,
                            label="Select Model",
                            label_style=text.body_medium(app.theme_mode),
                            border_color=COLORS["ui"][app.theme_mode.value]["primary"],
                            options=[
                                ft.dropdown.Option(
                                    key=name, # model class name as key
                                    text=model_name_str(name) # model name converted to display string as text
                                )
                                for name in models.keys()
                            ],
                            on_select=lambda e: save_model(e),
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 6,
                            },
                            expand=True
                        ),
                        ft.Text(
                            value=model_status_text,
                            style=text.body_medium(app.theme_mode, color=model_status_color_text, bold=True),
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 6,
                            }
                        )
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )

def model(
        app,
    ):

    return BasePage(
        app,
        title="Model",
        description="Define the model for the simulation",
        primary_content=ModelContent(app)
    )