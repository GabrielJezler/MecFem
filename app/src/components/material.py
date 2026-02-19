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
    
    def model_status_color_str(saved:bool=True):
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
    model_status_color_span, set_model_status_color_span = ft.use_state(model_status_color_str(False))
    model_name_span, set_model_name_span = ft.use_state(model_name_str(None))
    model_parameters_span, set_model_parameters_span = ft.use_state(model_parameters_str())
    model_name_dropdown, set_model_name_dropdown = ft.use_state(dropdown_model_str(None))
    parameter_controls, set_parameter_controls = ft.use_state([])

    parameters_ref = ft.use_ref(ft.Ref[ft.ResponsiveRow]())
    models_names_refs = ft.use_ref(None)

    def no_model_dialog():
        dialog = ft.AlertDialog(
            title=ft.Text(
                "No model selected", 
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

    def restore_state():
        if not app.simulation_data.material:
            return

        set_model_status_span(model_status_str(True))
        set_model_status_color_span(model_status_color_str(True))

        initial_model_name = app.simulation_data.material.__class__.__name__
        initial_params = {name: getattr(app.simulation_data.material, name) for name in get_model_parameters(app.simulation_data.material.__class__)[1:] if hasattr(app.simulation_data.material, name)}
        if initial_model_name:
            model = models.get(initial_model_name)
            if model:
                set_model_name_span(model_name_str(initial_model_name))
                set_model_parameters_span(model_parameters_str(initial_params))
                set_model_name_dropdown(dropdown_model_str(initial_model_name))

                update_parameter_controls(initial_params)

                models_names_refs.current = initial_model_name

    ft.on_mounted(restore_state)

    def update_from_material_model(e:ft.ControlEvent) -> None:
        model_name = e.control.value
        model = models.get(model_name)

        # Reset the material
        app.simulation_data.material = None
        set_model_parameters_span(model_parameters_str(None))
        set_model_status_span(model_status_str(False)) 
        set_model_status_color_span(model_status_color_str(False))

        if model:
            set_model_name_dropdown(dropdown_model_str(model_name))
            set_model_name_span(model_name_str(model_name))
            
            models_names_refs.current = model_name
            params_names = get_model_parameters(model)[1:]
            
            update_parameter_controls({name: None for name in params_names})
            if not params_names:
                set_model_parameters_span(model_parameters_str({}))
                set_model_name_dropdown(dropdown_model_str(None))
                models_names_refs.current = None
        else:
            set_model_name_dropdown(dropdown_model_str(None))
            set_model_name_span(model_name_str(None))

            set_parameter_controls([])
            models_names_refs.current = None

    def save_material(e: ft.ControlEvent)-> None:
        model_name = models_names_refs.current
        model = models.get(model_name)
        if not model:
            no_model_dialog()
            return
        
        params = {}
        for control in parameters_ref.current.controls:
            param_name = control.data
            param_value = control.value
            if not param_value:
                return # Do not update if any parameter is empty
            params[param_name] = float(param_value)
        
        try:
            material_instance = model(*params.values())
            app.simulation_data.material = material_instance
            set_model_parameters_span(model_parameters_str(params))
            set_model_status_span(model_status_str(True))
            set_model_status_color_span(model_status_color_str(True))
        except Exception as ex:
            material_not_saved_dialog(ex)

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