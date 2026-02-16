import flet as ft
import inspect
import pkgutil
import importlib

import MecFEM as mf

from utils import tomltools, stringtools
from themes import text
from ._base import BasePage

class MaterialContent(ft.Container):
    def __init__(self, page:ft.Page):
        super().__init__()

        self.COLORS = tomltools.load_colors()

        self.padding = 2
        self.models = self.get_material_models()
        self.expand = True

        self.material_drowpdown = ft.Dropdown(
            label="Select Material Model",
            label_style=text.body_medium(page),
            border_color=self.COLORS["ui"][page.theme_mode.value]["primary"],
            options=[
                ft.dropdown.Option(
                    key=model_name, 
                    text=stringtools.pascal_to_string(model_name)
                ) 
                for model_name in self.models.keys()
            ],
            on_select=lambda e: self.update_material_parameters(e),
            # expand=True
        )

        self.material_parameters_text = ft.Text("Select a material model to view its parameters.", style=text.body_medium(page))

        self.material_parameters = ft.ResponsiveRow(
            controls=[],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.content = ft.Column(
            controls=[
                self.material_drowpdown,
                self.material_parameters_text,
                self.material_parameters
            ],
            alignment=ft.MainAxisAlignment.START,
        )
    
    def update_material_parameters(self, e:ft.ControlEvent):
        model_name = e.control.value
        model = self.models.get(model_name)
        if model:
            params = self.get_model_parameters(model)[1:]
            if params:
                self.material_parameters_text.value = f"Parameters for {model_name} model: "
                self.material_parameters_text.spans = [
                    ft.TextSpan(
                        text=', '.join(params),
                        style=text.body_medium(self.page, color=self.COLORS["ui"][self.page.theme_mode.value]["primary"], bold=True)
                    )
                ]

                self.material_parameters.controls = [
                    ft.TextField(
                        label=param, 
                        label_style=text.body_medium(self.page),
                        border_color=self.COLORS["ui"][self.page.theme_mode.value]["primary"],
                        col={
                            ft.ResponsiveRowBreakpoint.XS: 12,
                            ft.ResponsiveRowBreakpoint.MD: 6,
                        },
                    ) for param in params
                ]
                self.material_parameters.data = params
            else:
                self.material_parameters_text.value = f"No parameters for {model_name}"
        else:
            self.material_parameters_text.value = "Select a material model to view its parameters."
        
        self.page.update()

    def get_material_models(self) -> dict[str, type]:
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

    def get_model_parameters(self, model: type) -> list[str] | None:
        if model:
            return list(inspect.signature(model.__init__).parameters.keys())
        return None

def material(
        page:ft.Page,
        title: str | None=None,
        description: str | None=None
    ):

    return BasePage(
        page=page,
        title=title,
        description=description,
        primary_content=MaterialContent(page=page)
    )