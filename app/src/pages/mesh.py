import flet as ft
import flet_charts
import matplotlib.pyplot as plt
import os
import asyncio

import MecFEM as mf

from utils import tomltools
from themes import text
from ._base import BasePage

@ft.component
def MeshContent(app) -> ft.Control:
    COLORS = tomltools.load_colors()

    mesh_path_text, set_mesh_path_text = ft.use_state("Select a mesh file (.msh)")
    fig, ax = plt.subplots()
    mesh_fig, set_mesh_fig = ft.use_state(fig)

    dim_ref = ft.Ref[ft.TextField]()
    mesh_path_ref = ft.Ref[ft.Container]()

    # def get_mesh_figure(mesh:mf.mesh.mesh_struct.Mesh):
    #     fig, ax = plt.subplots()

    #     mf.mesh.plot_mesh(mesh, ax=ax, nodes_ids=False, elems_ids=False, zoom_out=0.25)

    #     selector = mf.boundary_conditions.selection.RectangleSelector(ax)

    #     return fig, ax

    def show_file_error_dialog():
        dialog = ft.AlertDialog(
            title=ft.Text(
                "Invalid file type", 
                style=text.title_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["primary"])
            ),
            content=ft.Text("Please select a .msh file.", style=text.body_medium(app.theme_mode)),
            actions=[
                ft.TextButton(
                    "OK",

                    on_click=lambda e: ft.context.page.pop_dialog()
                )
            ],
            modal=True,
        )
        ft.context.page.show_dialog(dialog)

    async def handle_get_directory_path(e: ft.ControlEvent):
        files = await ft.FilePicker().pick_files()
        if files:
            if files[0].path.endswith((".msh")):
                app.simulation_data.mesh_path = files[0].path
                set_mesh_path_text(os.path.split(files[0].path)[-1])
            else:
                show_file_error_dialog()

    def show_mesh(e: ft.ControlEvent):
        if app.simulation_data.mesh_path is not None and dim_ref.current.value is not None:
            print("Plotting mesh...")
            print(f"Mesh path: {app.simulation_data.mesh_path}")
            print(f"Mesh dimension: {dim_ref.current.value}")
            try:
                mesh = mf.mesh.read.read_gmsh_mesh(app.simulation_data.mesh_path, dim=int(dim_ref.current.value))
                # fig, ax = get_mesh_figure(mesh)

                # ax = mf.mesh.plot_mesh(mesh, ax=ax, nodes_ids=False, elems_ids=False, zoom_out=0.25)

                # sel = mf.boundary_conditions.selection.RectangleSelector(ax)

                # set_mesh_fig(fig)
                print("Mesh plotted successfully.")
            except Exception as ex:
                print(f"Error plotting mesh: {ex}")

    return ft.Container(
        expand = True,
        padding = 2,
        content=ft.Column(
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            ref=mesh_path_ref,
                            content=ft.Text(mesh_path_text, style=text.body_medium(app.theme_mode), expand=True),
                            border=ft.Border.all(1, COLORS["ui"][app.theme_mode.value]["primary"]),
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
                            label="Mesh Dimension",
                            label_style=text.body_medium(app.theme_mode),
                            border_color=COLORS["ui"][app.theme_mode.value]["primary"],
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
                        ),
                        ft.TextButton(
                            content=ft.Text("Plot Mesh", style=text.body_medium(app.theme_mode)),
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
                    height=48
                ),
                flet_charts.MatplotlibChart(
                    figure=mesh_fig,
                    expand=True,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )
    
@ft.component
def mesh(
        app,
    ):

    return BasePage(
        app,
        title="Mesh",
        description="Manage meshes for your model.",
        primary_content=MeshContent(app)
    )