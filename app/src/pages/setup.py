import flet as ft
import inspect
import pkgutil
import importlib
import asyncio

import MecFEM as mf

from utils import stringtools
import themes
from components import ErrorDialog, Panel
from components.charts import MeshBoundaryElementsChart, MeshVolumeElementsChart
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

    return ft.ResponsiveRow(
        spacing=8,
        expand=True,
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        padding=8,
                        border_radius=16,
                        bgcolor=theme.colors["bg"],
                        content=ft.Dropdown(
                            ref=model_dropdown_ref,
                            value=model_name_text,
                            label="Select Model",
                            label_style=themes.text.body_medium(theme.mode),
                            border_color=theme.colors["bg_01"],
                            border_width=2,
                            border_radius=8,
                            options=[
                                ft.DropdownOption(
                                    text=model_name_str(name)
                                )
                                for name in MODELS.keys()
                            ],
                            on_select=lambda e: save_model(e),
                            expand=True,
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        padding=8,
                        bgcolor=theme.colors["bg"],
                        border_radius=16,
                        content=ft.Column(
                            controls=[
                                ft.Text("Boundary conditions:", style=themes.text.title_medium(theme.mode)),
                                ft.ListView(
                                    controls=[
                                        Panel(
                                            ft.Text("Panel title"),
                                            ft.Text("Expanded content"),
                                            expand_panel=False,
                                            selected=False,
                                        ) for _ in range(3)
                                    ],
                                    spacing=8,
                                    expand=True
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            expand=True,
                        ),
                        alignment=ft.Alignment.CENTER,
                    ),
                ],
                spacing=8,
                col={
                    ft.ResponsiveRowBreakpoint.SM: 12,
                    ft.ResponsiveRowBreakpoint.MD: 4,
                },
                expand=True,
            ),
            ft.Container(
                expand=True,
                bgcolor=theme.colors["bg"],
                border_radius=16,
                alignment=ft.Alignment.CENTER,
                padding=8,
                content=ft.Tabs(
                    length=2,
                    selected_index=0,
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.TabBar(
                                indicator_color=theme.colors["primary"],
                                tabs=[
                                    ft.Tab(
                                        label=ft.Text("External forces", style=themes.text.body_medium(theme.mode, bold=False)),
                                    ),
                                    ft.Tab(
                                        label=ft.Text("Volumetric forces", style=themes.text.body_medium(theme.mode, bold=False)),
                                    ),
                                ],
                            ),
                            ft.TabBarView(
                                expand=True,
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.SegmentedButton(
                                                allow_multiple_selection=False,
                                                selected=["none"],
                                                segments=[
                                                    ft.Segment(
                                                        value="none",
                                                        label=ft.Text("None"),
                                                    ),
                                                    ft.Segment(
                                                        value="rectangular",
                                                        label=ft.Text("Rectangular"),
                                                        icon=ft.Icon(ft.CupertinoIcons.RECTANGLE),
                                                    ),
                                                    ft.Segment(
                                                        value="lasso",
                                                        label=ft.Text("Lasso"),
                                                        icon=ft.Icon(ft.CupertinoIcons.LASSO),
                                                    ),
                                                ],
                                                show_selected_icon=False,
                                                style=ft.ButtonStyle(
                                                    color={
                                                        ft.ControlState.DEFAULT: theme.colors["text"],
                                                        ft.ControlState.SELECTED: theme.colors["text"],
                                                    },
                                                    bgcolor={
                                                        ft.ControlState.DEFAULT: theme.colors["bg"],
                                                        ft.ControlState.SELECTED: theme.colors["bg_01"],
                                                    },
                                                    shape=ft.RoundedRectangleBorder(radius=8),
                                                    text_style=themes.text.body_small(theme.mode, bold=True),
                                                    side=ft.BorderSide(2, theme.colors["bg_01"]),
                                                ),
                                            ),
                                            ft.Container(
                                                border_radius=8,
                                                border=ft.Border.all(2, theme.colors["bg_01"]),
                                                content=MeshBoundaryElementsChart(),
                                                alignment=ft.Alignment.CENTER,
                                                padding=0,
                                                expand=True,
                                            ),
                                        ],
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.SegmentedButton(
                                                allow_multiple_selection=False,
                                                selected=["none"],
                                                segments=[
                                                    ft.Segment(
                                                        value="none",
                                                        label=ft.Text("None"),
                                                    ),
                                                    ft.Segment(
                                                        value="rectangular",
                                                        label=ft.Text("Rectangular"),
                                                        icon=ft.Icon(ft.CupertinoIcons.RECTANGLE),
                                                    ),
                                                    ft.Segment(
                                                        value="lasso",
                                                        label=ft.Text("Lasso"),
                                                        icon=ft.Icon(ft.CupertinoIcons.LASSO),
                                                    ),
                                                ],
                                                show_selected_icon=False,
                                                style=ft.ButtonStyle(
                                                    color={
                                                        ft.ControlState.DEFAULT: theme.colors["text"],
                                                        ft.ControlState.SELECTED: theme.colors["text"],
                                                    },
                                                    bgcolor={
                                                        ft.ControlState.DEFAULT: theme.colors["bg"],
                                                        ft.ControlState.SELECTED: theme.colors["bg_01"],
                                                    },
                                                    shape=ft.RoundedRectangleBorder(radius=8),
                                                    text_style=themes.text.body_small(theme.mode, bold=True),
                                                    side=ft.BorderSide(2, theme.colors["bg_01"]),
                                                ),
                                            ),
                                            ft.Container(
                                                border_radius=8,
                                                border=ft.Border.all(2, theme.colors["bg_01"]),
                                                content=MeshVolumeElementsChart(),
                                                alignment=ft.Alignment.CENTER,
                                                padding=0,
                                                expand=True,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),
                col={
                    ft.ResponsiveRowBreakpoint.SM: 12,
                    ft.ResponsiveRowBreakpoint.MD: 8,
                },
            )
        ]
    )
