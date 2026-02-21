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
def MaterialContent(app) -> ft.Control:
    def material_status_str(saved:bool=True):
        if saved:
            return "Material model saved."
        return "No material model saved."
    
    def material_status_color_str(saved:bool=True):
        if saved:
            return COLORS["ui"][app.theme_mode.value]["success"]
        return COLORS["ui"][app.theme_mode.value]["alert"]
    
    def material_name_str(model_name:str | None=None):
        if model_name:
            return stringtools.pascal_to_string(model_name)
        return "None"

    def material_parameters_str(params:dict[str, str] | None=None):
        if params:
            return ", ".join([f"{name} = {value}" for name, value in params.items()])
        elif params == {}:
            return "Selected model has no parameters."
        elif params is None:
            return ""

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

    COLORS = tomltools.load_colors()
    materials = get_materials()

    material_status_span, set_material_status_span = ft.use_state(material_status_str(False))
    material_status_color_span, set_material_status_color_span = ft.use_state(material_status_color_str(False))
    material_parameters_span, set_material_parameters_span = ft.use_state(material_parameters_str())

    material_name_dropdown, set_material_name_dropdown = ft.use_state(dropdown_material_str(None))
    material_name_data_dropdown, set_material_name_data_dropdown = ft.use_state(None)
    parameter_controls, set_parameter_controls = ft.use_state([])

    parameters_ref = ft.use_ref(ft.Ref[ft.ResponsiveRow]())
    dropdown_ref = ft.use_ref(ft.Ref[ft.Dropdown]())

    def no_material_dialog():
        dialog = ft.AlertDialog(
            title=ft.Text(
                "No material selected", 
                style=text.title_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["primary"])
            ),
            content=ft.Text(
                "Please select a material model before saving.", 
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

    def material_not_saved_dialog(exception: Exception = None):
        dialog = ft.AlertDialog(
            title=ft.Text(
                "Material not saved", 
                style=text.title_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["primary"])
            ),
            content=ft.Text(
                f"Please fill in all parameters and save the material model before proceeding.", 
                spans=[
                    ft.TextSpan(
                        text=f"\nError details: {exception}",
                        style=text.body_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["alert"], italic=True)
                    )
                ] if exception else None,
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

    def update_parameter_controls(params_names: dict[str, str] | None):
        if params_names:            
            set_parameter_controls(
                [
                    ft.TextField(
                        label=param,
                        data=param,
                        key=param,
                        value=params_names.get(param, None),
                        label_style=text.body_medium(app.theme_mode),
                        border_color=COLORS["ui"][app.theme_mode.value]["primary"],
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
                    ) for param in params_names
                ]
            )
        else:
            set_parameter_controls([])

    def update_from_material_model(e:ft.ControlEvent) -> None:
        material_name = e.control.value
        material = materials.get(material_name)

        # Reset the material
        app.simulation_data.material = None
        set_material_parameters_span(material_parameters_str(None))
        set_material_status_span(material_status_str(False)) 
        set_material_status_color_span(material_status_color_str(False))

        if material:
            set_material_name_dropdown(dropdown_material_str(material_name))
            set_material_name_data_dropdown(material_name)

            params_names = get_material_parameters(material)[1:]
            
            update_parameter_controls({name: None for name in params_names})
            if not params_names:
                set_material_parameters_span(material_parameters_str({}))
                set_material_name_dropdown(dropdown_material_str(None))
                set_material_name_data_dropdown(None)
        else:
            set_material_name_dropdown(dropdown_material_str(None))
            set_material_name_data_dropdown(None)
            set_parameter_controls([])

    def save_material(e: ft.ControlEvent)-> None:
        material_name = dropdown_ref.current.data
        material = materials.get(material_name)
        if not material:
            no_material_dialog()
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
            app.simulation_data.material = material_instance
            set_material_parameters_span(material_parameters_str(params))
            set_material_status_span(material_status_str(True))
            set_material_status_color_span(material_status_color_str(True))
        except Exception as ex:
            material_not_saved_dialog(ex)

    def mount():
        if not app.simulation_data.material:
            return

        set_material_status_span(material_status_str(True))
        set_material_status_color_span(material_status_color_str(True))

        initial_material_name = app.simulation_data.material.__class__.__name__
        initial_params = {name: getattr(app.simulation_data.material, name) for name in get_material_parameters(app.simulation_data.material.__class__)[1:] if hasattr(app.simulation_data.material, name)}
        if initial_material_name:
            material = materials.get(initial_material_name)
            if material:
                set_material_parameters_span(material_parameters_str(initial_params))
                set_material_name_dropdown(dropdown_material_str(initial_material_name))
                set_material_name_data_dropdown(initial_material_name)

                update_parameter_controls(initial_params)

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
                            ref=dropdown_ref,
                            value=material_name_dropdown,
                            data=material_name_data_dropdown,
                            label="Select Material Model",
                            label_style=text.body_medium(app.theme_mode),
                            border_color=COLORS["ui"][app.theme_mode.value]["primary"],
                            options=[
                                ft.dropdown.Option(
                                    key=material_name, 
                                    text=stringtools.pascal_to_string(material_name)
                                ) 
                                for material_name in materials.keys()
                            ],
                            on_select=lambda e: update_from_material_model(e),
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 4,
                            },
                            expand=True
                        ),
                        ft.Text(
                            spans=[
                                ft.TextSpan(
                                    text=material_status_span,
                                    style=text.body_medium(app.theme_mode, color=material_status_color_span, bold=True),
                                ),
                                ft.TextSpan(
                                    text="\nMaterial parameters: ",
                                    style=text.body_medium(app.theme_mode)
                                ),
                                ft.TextSpan(
                                    text=material_parameters_span,
                                    style=text.body_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["primary"], bold=True)
                                )
                            ],
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 8,
                            }
                        )
                    ]
                ),
                ft.ResponsiveRow(
                    ref=parameters_ref,
                    controls=parameter_controls,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )

def material(
        app,
    ):

    return BasePage(
        app,
        title="Material",
        description="Manage materials for your model.",
        primary_content=MaterialContent(app)
    )