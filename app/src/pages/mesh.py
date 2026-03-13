import flet as ft
import os
import asyncio

import MecFEM as mf

from themes import text
from components import BasePage, ErrorDialog
from components.charts import MeshChart
from contexts import *

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

    def show_mesh(e: ft.ControlEvent):
        mesh_path = mesh_path_ref.current.data
        dim = dim_ref.current.value

        if mesh_path and dim:
            try:
                mesh = mf.mesh.Mesh(mesh_path, dim=int(dim))
                print(f"Mesh loaded")
                if simulation.state.mesh != mesh:
                    simulation.state.mesh = mesh
                print(f"Mesh set in simulation state")

            except Exception as ex:
                ErrorDialog(theme, "Error plotting mesh", f"ERROR: {ex}")

    def mount():
        if simulation.state.mesh is not None:
            set_mesh_path_text(os.path.split(simulation.state.mesh.filename)[-1])
            set_mesh_fullpath_text(simulation.state.mesh.filename)
            set_dim_text(str(simulation.state.mesh.dim))

    ft.use_effect(mount, [])

    return ft.Container(
        expand=True,
        padding=2,
        content=ft.Column(
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            ref=mesh_path_ref,
                            content=ft.Text(mesh_path_text, style=text.body_medium(theme.mode), expand=True),
                            data=mesh_fullpath_text,
                            border=ft.Border.all(1, theme.colors["primary"]),
                            border_radius=4,
                            padding=ft.Padding(16, 12, 16, 12),
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 12,
                                ft.ResponsiveRowBreakpoint.LG: 6,
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
                            border_color=theme.colors["primary"],
                            col={
                                ft.ResponsiveRowBreakpoint.XS: 12,
                                ft.ResponsiveRowBreakpoint.MD: 6,
                                ft.ResponsiveRowBreakpoint.LG: 4,
                            },
                            input_filter=ft.InputFilter(
                                regex_string=r"^[1-3]?$",
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
                ft.Container(
                    bgcolor=theme.colors["bg_secondary"],
                    border_radius=24,
                    content=MeshChart(simulation.state.mesh),
                    alignment=ft.Alignment.CENTER,
                    padding=0,
                    # margin=ft.Margin(8, 8, 8, 8),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        ),
    )

@ft.component
def mesh():
    return BasePage(
        title="Mesh",
        primary_content=MeshContent()
    )