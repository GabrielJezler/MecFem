import flet as ft
import os
import asyncio

import MecFEM as mf

from themes import text
from components import ErrorDialog, Tooltip
from components.charts import MeshChart
from structures.contexts import ThemeContext, SimulationContext

@ft.component
def MeshContent() -> ft.Control:
    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    mesh_path_text, set_mesh_path_text = ft.use_state("Select a mesh file (.msh)")
    mesh_fullpath_text, set_mesh_fullpath_text = ft.use_state(None)
    dim_text, set_dim_text = ft.use_state(None)
    
    dim_ref = ft.Ref[ft.TextField]()
    mesh_path_ref = ft.Ref[ft.Container]()

    async def handle_get_directory_path(e: ft.ControlEvent):
        files = await ft.FilePicker().pick_files()
        if files:
            if files[0].path.endswith((".msh")):
                set_mesh_path_text(os.path.split(files[0].path)[-1])
                set_mesh_fullpath_text(files[0].path)
            else:
                ErrorDialog(theme, "Invalid file type", "Please select a .msh file.")

    async def handle_reset(e: ft.Event[ft.Button]):
        await viewer.reset(animation_duration=ft.Duration(milliseconds=500))

    def show_mesh(e: ft.ControlEvent):
        mesh_path = mesh_path_ref.current.data
        dim = dim_ref.current.value

        if mesh_path and dim:
            try:
                mesh = mf.mesh.Mesh(mesh_path, dim=int(dim))
                if simulation.state.mesh != mesh:
                    simulation.state.mesh = mesh
            except Exception as ex:
                ErrorDialog(theme, "Error plotting mesh", f"ERROR: {ex}")

    def mount():
        if simulation.state.mesh is not None:
            set_mesh_path_text(os.path.split(simulation.state.mesh.filename)[-1])
            set_mesh_fullpath_text(simulation.state.mesh.filename)
            set_dim_text(str(simulation.state.mesh.dim))

    ft.use_effect(mount, [])

    return ft.Column(
        controls=[
            ft.Container(
                padding=8,
                border_radius=16,
                bgcolor=theme.colors["bg"],
                content=ft.ResponsiveRow(
                    controls=[
                        ft.Text(
                            "Mesh",
                            style=text.title_medium(theme.mode),
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 3,
                                ft.ResponsiveRowBreakpoint.MD: 2,
                                ft.ResponsiveRowBreakpoint.LG: 1,
                            },
                        ),
                        ft.Container(
                            ref=mesh_path_ref,
                            content=ft.Text(
                                mesh_path_text, 
                                style=text.body_medium(theme.mode,), 
                                expand=True
                            ),
                            data=mesh_fullpath_text,
                            border=ft.Border.all(2, theme.colors["bg_01"]),
                            border_radius=8,
                            padding=ft.Padding(16, 12, 16, 12),
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 9,
                                ft.ResponsiveRowBreakpoint.MD: 10,
                                ft.ResponsiveRowBreakpoint.LG: 7,
                            },
                            expand=True,
                            height=48,
                            on_click=lambda e: asyncio.create_task(handle_get_directory_path(e)),
                        ),
                        ft.TextField(
                            ref=dim_ref,
                            value=dim_text,
                            label="Mesh Dimension",
                            label_style=text.body_medium(theme.mode),
                            border_color=theme.colors["bg_01"],
                            border_width=2,
                            border_radius=8,
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 6,
                                ft.ResponsiveRowBreakpoint.LG: 2,
                            },
                            input_filter=ft.InputFilter(
                                regex_string=r"^[1-2]?$",
                                allow=True,
                                replacement_string="",
                            ),
                            expand=True,
                            height=48,
                            on_submit=lambda e: set_dim_text(dim_ref.current.value),
                        ),
                        ft.TextButton(
                            content=ft.Text("Plot Mesh"),
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 6,
                                ft.ResponsiveRowBreakpoint.LG: 2,
                            },
                            expand=True,
                            height=48,
                            on_click=lambda e: show_mesh(e),
                        )
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                expand=True,
                padding=8,
                border_radius=16,
                bgcolor=theme.colors["bg"],
                content=ft.Stack(
                    expand=True,
                    controls=[
                        viewer := ft.InteractiveViewer(
                            # min_scale=0.1,
                            # max_scale=10,
                            expand=True,
                            content=ft.Container(
                                content=ft.Container() if simulation.state.mesh is None else MeshChart(),
                            ),
                        ),
                        ft.FloatingActionButton(
                            icon=ft.Icon(
                                ft.CupertinoIcons.ARROW_CLOCKWISE,
                                color=theme.colors["text"],
                            ),
                            bgcolor=theme.colors["bg_01"],
                            margin=0,
                            mini=True,
                            shape=ft.RoundedRectangleBorder(radius=16),
                            tooltip=Tooltip(
                                message="Reset view",
                                wait_duration=ft.Duration(seconds=1),
                            ),
                            on_click=lambda e: asyncio.create_task(handle_reset(e)),
                        ),
                    ]
                ),
                alignment=ft.Alignment.CENTER,
            ),
        ],
        spacing=8,
        expand=True,
    )
