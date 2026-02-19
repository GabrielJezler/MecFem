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
    def model_status_str(saved:bool=True):
        if saved:
            return "Material model saved."
        return "No material model saved."
    
    def model_status_color(saved:bool=True):
        if saved:
            return COLORS["ui"][app.theme_mode.value]["success"]
        return COLORS["ui"][app.theme_mode.value]["alert"]
    
    def model_name_str(model_name:str | None=None):
        if model_name:
            return stringtools.pascal_to_string(model_name)
        return "None"

    def model_parameters_str(params:dict[str, str] | None=None):
        if params:
            return ", ".join([f"{name} = {value}" for name, value in params.items()])
        elif params == {}:
            return "Selected model has no parameters."
        elif params is None:
            return ""

    def dropdown_model_str(model_name: str | None = None):
        if model_name:
            return model_name
        return None


    def get_model_parameters(model: type) -> list[str] | None:
        if model:
            return list(inspect.signature(model.__init__).parameters.keys())
        return None

    def get_material_models() -> dict[str, type]:
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
    models = get_material_models()

    model_status_span, set_model_status_span = ft.use_state(model_status_str(False))
    model_status_color_span, set_model_status_color_span = ft.use_state(model_status_color(False))
    model_name_span, set_model_name_span = ft.use_state(model_name_str(None))
    model_parameters_span, set_model_parameters_span = ft.use_state(model_parameters_str())
    model_name_dropdown, set_model_name_dropdown = ft.use_state(dropdown_model_str(None))

    parameter_controls, set_parameter_controls = ft.use_state([]) 
    
    params_refs = ft.use_ref({}) # Refs for the parementer's name and control, used to get the current value of the parameter fields when saving the material
    models_names_refs = ft.use_ref({}) # Ref for the model's name and control, used to reset the dropdown value when a model is deselected

    def restore_state():
        if not app.simulation_data.material:
            return

        set_model_status_span(model_status_str(True))
        set_model_status_color_span(model_status_color(True))

        initial_model_name = app.simulation_data.material.__class__.__name__
        initial_params = {name: getattr(app.simulation_data.material, name) for name in get_model_parameters(app.simulation_data.material.__class__)[1:] if hasattr(app.simulation_data.material, name)}
        if initial_model_name:
            model = models.get(initial_model_name)
            if model:
                set_model_name_dropdown(dropdown_model_str(initial_model_name))
                set_model_status_span(model_status_str(True))

                set_model_name_span(model_name_str(initial_model_name))
                set_model_parameters_span(model_parameters_str(initial_params))

                models_names_refs.current = {initial_model_name: None}
                params_names = initial_params.keys()
                
                if params_names:
                    new_refs = {}
                    new_controls = []
                    for param in params_names:
                        ref = ft.Ref[ft.TextField]()
                        new_refs[param] = ref
                        
                        # Get saved value or default to empty
                        saved_value = initial_params.get(param, "")
                        
                        new_controls.append(
                            ft.TextField(
                                ref=ref,
                                label=param,
                                value=str(saved_value),  # Restore saved value
                                data=param,
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
                            )
                        )
                    
                    params_refs.current = new_refs
                    set_parameter_controls(new_controls)

    ft.on_mounted(restore_state)

    def update_material_parameters(e:ft.ControlEvent) -> None:
        model_name = e.control.value
        model = models.get(model_name)

        # Reset the material
        app.simulation_data.material = None
        set_model_parameters_span(model_parameters_str(None))
        set_model_status_span(model_status_str(False)) 
        set_model_status_color_span(model_status_color(False))

        if model:
            set_model_name_dropdown(dropdown_model_str(model_name))
            set_model_name_span(model_name_str(model_name))
            
            models_names_refs.current = {model_name: e.control}
            params_names = get_model_parameters(model)[1:]
            if params_names:
                new_refs = {}
                for param in params_names:
                    ref = ft.Ref[ft.TextField]()
                    new_refs[param] = ref

                params_refs.current = new_refs
                set_parameter_controls(
                    [
                        ft.TextField(
                            ref=ref,
                            label=param,
                            data=param,
                            key=param,
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
                        ) for param, ref in params_refs.current.items()
                    ]
                )
            else:
                set_model_parameters_span(model_parameters_str({}))
                set_parameter_controls([])
                set_model_name_dropdown(dropdown_model_str(None))
                params_refs.current = {}
                models_names_refs.current = {}
        else:
            set_model_name_span(model_name_str(None))
            set_parameter_controls([])
            set_model_name_dropdown(dropdown_model_str(None))
            params_refs.current = {}
            models_names_refs.current = {}

    def save_material(e: ft.ControlEvent)-> None:
        model_name = list(models_names_refs.current.keys())[0]
        model = models.get(model_name)
        if not model:
            raise ValueError("No model selected")
        
        params = {}
        for param_name, ref in params_refs.current.items():
            if ref.current:
                value = ref.current.value
                if not value or value.strip() == "":
                    return
                try:
                    params[param_name] = float(value)
                except ValueError:
                    return

        print(f"Saving material with model {model_name} and parameters: {params}")
        
        try:
            material_instance = model(*params.values())
            app.simulation_data.material = material_instance
            set_model_parameters_span(model_parameters_str(params))
            set_model_status_span(model_status_str(True))
            set_model_status_color_span(model_status_color(True))
        except Exception as ex:
            raise ValueError(f"Error creating material instance: {ex}")

    return ft.Container(
        expand = True,
        padding = 2,
        content = ft.Column(
            controls=[
                ft.ResponsiveRow(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Dropdown(
                            value=model_name_dropdown,
                            label="Select Material Model",
                            label_style=text.body_medium(app.theme_mode),
                            border_color=COLORS["ui"][app.theme_mode.value]["primary"],
                            options=[
                                ft.dropdown.Option(
                                    key=model_name, 
                                    text=stringtools.pascal_to_string(model_name)
                                ) 
                                for model_name in models.keys()
                            ],
                            on_select=lambda e: update_material_parameters(e),
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 4,
                            },
                            expand=True
                        ),
                        ft.Text(
                            spans=[
                                ft.TextSpan(
                                    text=model_status_span,
                                    style=text.body_medium(app.theme_mode, color=model_status_color_span, bold=True),
                                ),
                                ft.TextSpan(
                                    text="\nMaterial model: ",
                                    style=text.body_medium(app.theme_mode),
                                ),
                                ft.TextSpan(
                                    text=model_name_span,
                                    style=text.body_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["primary"], bold=True)
                                ),
                                ft.TextSpan(
                                    text="\nMaterial parameters: ",
                                    style=text.body_medium(app.theme_mode)
                                ),
                                ft.TextSpan(
                                    text=model_parameters_span,
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