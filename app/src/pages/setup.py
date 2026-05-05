import flet as ft
import inspect
import pkgutil
import importlib

import MecFEM as mf

from utils import stringtools
import themes
from components import ErrorDialog, Panel
from components.charts import MeshSelectorChart
from structures.contexts import ThemeContext, SimulationContext, SelectorContext, OrientationContext
from structures.chart import RetangularSelectorMode, LassoSelectorMode, Selector
from structures.enums import MeshSelectionShape, MeshSelectionObject, MeshSelectionZone

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

    def update_selection_mode(e: ft.ControlEvent):
        new_mode = list(MeshSelectionShape)[e.data]
        if new_mode != selector_id:
            set_selector_id(e.data)
    
    def update_selection_zone(e: ft.ControlEvent):
        new_zone = list(MeshSelectionZone)[e.data]
        if new_zone != selection_region_id:
            set_selection_region_id(e.data)
        
    def update_selection_object(e: ft.ControlEvent):
        new_object = list(MeshSelectionObject)[e.data]
        if new_object != selection_object_id:
            set_selection_object_id(e.data)

    def get_selector(mode_id: MeshSelectionShape, zone_id: MeshSelectionZone, object_id: MeshSelectionObject):
        shape = list(MeshSelectionShape)[mode_id]
        zone = list(MeshSelectionZone)[zone_id]
        obj = list(MeshSelectionObject)[object_id]
        if shape == MeshSelectionShape.RECTANGLE:
            mode = RetangularSelectorMode()
        elif shape == MeshSelectionShape.LASSO:
            mode = LassoSelectorMode()
        else:
            mode = None

        return Selector(mode=mode, zone=zone, object=obj)

    def mount():
        if simulation.state.model:
            set_model_name_text(model_name_str(simulation.state.model.__class__.__name__))

    ft.use_effect(mount, [])

    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)
    orientation = ft.use_context(OrientationContext)

    MODELS = get_models()

    model_name_text, set_model_name_text = ft.use_state(model_name_str())

    selector_id, set_selector_id = ft.use_state(0)
    selection_region_id, set_selection_region_id = ft.use_state(0)
    selection_object_id, set_selection_object_id = ft.use_state(0)

    selector_value = ft.use_memo(
        lambda: get_selector(selector_id, selection_region_id, selection_object_id),
        dependencies=[selector_id, selection_region_id, selection_object_id],
    )

    return SelectorContext(
        selector_value,
        lambda : ft.ResponsiveRow(
            spacing=8,
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Container(
                            padding=8,
                            border_radius=16,
                            bgcolor=theme.colors["bg"],
                            content=ft.Row(
                                expand=True,
                                controls=[
                                    ft.Text(
                                        "Model", 
                                        style=themes.text.title_medium(theme.mode),
                                    ),
                                    ft.Dropdown(
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
                                ]
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            padding=8,
                            bgcolor=theme.colors["bg"],
                            border_radius=16,
                            content=ft.Column(
                                controls=[
                                    ft.Text("Boundary conditions", style=themes.text.title_medium(theme.mode)),
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
                ),
                ft.Container(
                    expand=True,
                    bgcolor=theme.colors["bg"],
                    border_radius=16,
                    padding=8,
                    content=ft.Column(
                        expand=True,
                        margin=0,
                        controls=[
                            ft.ResponsiveRow(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                margin=0,
                                columns=24,
                                controls=[
                                    ft.Row(
                                        spacing=8,
                                        alignment=ft.MainAxisAlignment.START,
                                        controls=[
                                            # ft.Text("Region:", style=themes.text.body_medium(theme.mode, bold=False)),
                                            ft.CupertinoSlidingSegmentedButton(
                                                expand=True,
                                                padding=ft.Padding.symmetric(vertical=3, horizontal=8),
                                                bgcolor=ft.Colors.with_opacity(0.5, theme.colors["bg_01"]),
                                                thumb_color=theme.colors["primary"],
                                                selected_index=selection_region_id,
                                                controls=[
                                                    ft.Text(mode.value, style=themes.text.body_small(theme.mode, bold=True)) for mode in MeshSelectionZone
                                                ],
                                                on_change=lambda e: update_selection_zone(e),
                                            ),
                                        ],
                                        col={
                                            ft.ResponsiveRowBreakpoint.XS: 24,
                                            ft.ResponsiveRowBreakpoint.SM: 12,
                                            ft.ResponsiveRowBreakpoint.XL: 7,
                                        }
                                    ),
                                    ft.Row(
                                        spacing=8,
                                        alignment=ft.MainAxisAlignment.START,
                                        controls=[
                                            # ft.Text("Object:", style=themes.text.body_medium(theme.mode, bold=False)),
                                            ft.CupertinoSlidingSegmentedButton(
                                                expand=True,
                                                padding=ft.Padding.symmetric(vertical=3, horizontal=8),
                                                bgcolor=ft.Colors.with_opacity(0.5, theme.colors["bg_01"]),
                                                thumb_color=theme.colors["primary"],
                                                selected_index=selection_object_id,
                                                controls=[
                                                    ft.Text(mode.value, style=themes.text.body_small(theme.mode, bold=True)) for mode in MeshSelectionObject
                                                ],
                                                on_change=lambda e: update_selection_object(e),
                                            ),
                                        ],
                                        col={
                                            ft.ResponsiveRowBreakpoint.XS: 24,
                                            ft.ResponsiveRowBreakpoint.SM: 12,
                                            ft.ResponsiveRowBreakpoint.XL: 7,
                                        }
                                    ),
                                    ft.Row(
                                        spacing=8,
                                        alignment=ft.MainAxisAlignment.START,
                                        controls=[
                                            # ft.Text("Selector:", style=themes.text.body_medium(theme.mode, bold=False)),
                                            ft.CupertinoSlidingSegmentedButton(
                                                expand=True,
                                                padding=ft.Padding.symmetric(vertical=3, horizontal=8),
                                                bgcolor=ft.Colors.with_opacity(0.5, theme.colors["bg_01"]),
                                                thumb_color=theme.colors["primary"],
                                                selected_index=selector_id,
                                                controls=[
                                                    ft.Text(mode.value, style=themes.text.body_small(theme.mode, bold=True)) for mode in MeshSelectionShape
                                                ],
                                                on_change=lambda e: update_selection_mode(e),
                                            ),
                                        ],
                                        col={
                                            ft.ResponsiveRowBreakpoint.XS: 24,
                                            ft.ResponsiveRowBreakpoint.XL: 10,
                                        }
                                    ),
                                ]
                            ),
                            ft.Container(
                                border_radius=8,
                                border=ft.Border.all(2, theme.colors["bg_01"]),
                                content=MeshSelectorChart(),
                                alignment=ft.Alignment.CENTER,
                                padding=0,
                                expand=True,
                            ),
                        ],
                    ),
                    col={
                        ft.ResponsiveRowBreakpoint.SM: 12,
                        ft.ResponsiveRowBreakpoint.MD: 8,
                    },
                )
            ]
        ),
    )
