import flet as ft
import inspect
import pkgutil
import importlib

import MecFEM as mf

from utils import tomltools, stringtools
from themes import text
from components import BasePage, ErrorDialog
from contexts import *

@ft.component
def MaterialContent() -> ft.Control:
    def dropdown_material_str(model_name: str | None = None):
        if model_name:
            return model_name
        return ""

    def get_material_parameters(model: type) -> list[str] | None:
        if model:
            return list(inspect.signature(model.__init__).parameters.keys())
        return None

    def get_materials() -> dict[str, type]:
        models = {}

        for _, module_name, _ in pkgutil.walk_packages(
            mf.materials.__path__, mf.materials.__name__ + "."
        ):
            if "base" not in module_name.lower().split("."):
                module = importlib.import_module(module_name)

                for name, cls in inspect.getmembers(module, inspect.isclass):
                    if cls.__module__ == module.__name__:
                        models[name] = cls

        return models

    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    materials = get_materials()

    material_name_dropdown, set_material_name_dropdown = ft.use_state(dropdown_material_str(None))
    material_name_data_dropdown, set_material_name_data_dropdown = ft.use_state(None)
    parameters_names, set_parameters_names = ft.use_state({})

    parameters_ref = ft.use_ref(ft.Ref[ft.ResponsiveRow]())
    dropdown_ref = ft.use_ref(ft.Ref[ft.Dropdown]())

    def save_material(e: ft.ControlEvent)-> None:
        material_name = dropdown_ref.current.data
        material = materials.get(material_name)
        if not material:
            ErrorDialog(theme, "No material selected", "Please select a material model before saving.")
            return
        
        params = {}
        for control in parameters_ref.current.controls:
            param_name = control.data
            param_value = control.value
            if not param_value:
                return
            params[param_name] = float(param_value)
        
        try:
            material_instance = material(*params.values())
            if material_instance != simulation.state.material:
                simulation.state.model = None
                simulation.state.material = material_instance
        except Exception as ex:
            ErrorDialog(theme, "Material not saved", f"ERROR: {ex}")

    def update_from_material_model(e:ft.ControlEvent) -> None:
        material_name = e.control.value
        material = materials.get(material_name)

        if material.__name__ != simulation.state.material.__class__.__name__:
            simulation.state.model = None
            simulation.state.material = None

        if material:
            set_material_name_dropdown(dropdown_material_str(material_name))
            set_material_name_data_dropdown(material_name)

            params_names = get_material_parameters(material)[1:]
            
            set_parameters_names({name: None for name in params_names})
            if not params_names:
                set_material_name_dropdown(dropdown_material_str(None))
                set_material_name_data_dropdown(None)
        else:
            set_material_name_dropdown(dropdown_material_str(None))
            set_material_name_data_dropdown(None)
            set_parameters_names({})

    def mount():
        if not simulation.state.material:
            return

        initial_material_name = simulation.state.material.__class__.__name__
        initial_params = {name: getattr(simulation.state.material, name) for name in get_material_parameters(simulation.state.material.__class__)[1:] if hasattr(simulation.state.material, name)}
        if initial_material_name:
            material = materials.get(initial_material_name)
            if material:
                set_material_name_dropdown(dropdown_material_str(initial_material_name))
                set_material_name_data_dropdown(initial_material_name)

                set_parameters_names(initial_params)

    ft.use_effect(mount, [])

    return ft.Container(
        expand = True,
        padding = 2,
        content = ft.Column(
            controls=[
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Dropdown(
                            ref=dropdown_ref,
                            value=material_name_dropdown,
                            data=material_name_data_dropdown,
                            label="Select Material Model",
                            label_style=text.body_medium(theme.mode),
                            border_color=theme.colors["primary"],
                            options=[
                                ft.dropdown.Option(
                                    key=material_name, 
                                    text=stringtools.pascal_to_string(material_name)
                                ) 
                                for material_name in materials.keys()
                            ],
                            on_select=lambda e: update_from_material_model(e),
                            expand=True
                        ),
                    ]
                ),
                ft.ResponsiveRow(
                    ref=parameters_ref,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.TextField(
                            label=name,
                            data=name,
                            value=value,
                            label_style=text.body_medium(theme.mode),
                            border_color=theme.colors["primary"],
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 6,
                            },
                            input_filter=ft.InputFilter(
                                regex_string=r"^[0-9]*\.?[0-9]*$",
                                allow=True,
                                replacement_string="",
                            ),
                            on_submit=lambda e: save_material(e),
                        ) for name, value in parameters_names.items()
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )

def material():

    return BasePage(
        title="Material",
        primary_content=MaterialContent()
    )