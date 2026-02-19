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
    dim_text, set_dim_text = ft.use_state(None)
    mesh_status_str, set_mesh_status_str = ft.use_state("No mesh loaded.")
    mesh_status_path_str, set_mesh_status_path_str = ft.use_state(None)

    mesh_fig, set_mesh_fig = ft.use_state(None)

    dim_ref = ft.Ref[ft.TextField]()
    mesh_path_ref = ft.Ref[ft.Container]()

    def show_file_error_dialog():
        dialog = ft.AlertDialog(
            title=ft.Text(
                "Invalid file type", 
                # style=text.title_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["primary"])
            ),
            content=ft.Text(
                "Please select a .msh file.", 
                # style=text.body_medium(app.theme_mode)
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

    async def handle_get_directory_path(e: ft.ControlEvent):
        files = await ft.FilePicker().pick_files()
        if files:
            if files[0].path.endswith((".msh")):
                set_mesh_path_text(os.path.split(files[0].path)[-1])
                mesh_path_ref.current.data = files[0].path
            else:
                show_file_error_dialog()

    def show_mesh(e: ft.ControlEvent):
        mesh_path = mesh_path_ref.current.data
        dim = dim_ref.current.value
        if mesh_path is not None and dim is not None:
            print("Plotting mesh...")
            print(f"Mesh path: {mesh_path}")
            print(f"Mesh dimension: {dim}")
            try:
                mesh = mf.mesh.read.read_gmsh_mesh(mesh_path, dim=int(dim))

                app.simulation_data.mesh_path = mesh_path
                app.simulation_data.mesh = mesh

                set_mesh_status_str("Mesh loaded successfully: ")
                set_mesh_status_path_str(mesh_path)

                fig, ax = plt.subplots()

                ax = mf.mesh.plot_mesh(mesh, ax=ax, nodes_ids=False, elems_ids=False, zoom_out=0.25)

                sel = mf.boundary_conditions.selection.RectangleSelector(ax)

                plt.show()

                # set_mesh_fig(fig)
            except Exception as ex:
                print(f"Error plotting mesh: {ex}")

    if app.simulation_data.mesh_path is not None:
        mesh_path_text = os.path.split(app.simulation_data.mesh_path)[-1]
        set_mesh_path_text(mesh_path_text)

    if app.simulation_data.mesh is not None:
        set_dim_text(str(app.simulation_data.mesh.dim))

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
                            data=None if app.simulation_data.mesh_path is None else app.simulation_data.mesh_path,
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
                            value=dim_text,
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
                ft.Text(
                    mesh_status_str,
                    style=text.body_medium(app.theme_mode),
                    spans=[
                        ft.TextSpan(
                            text=mesh_status_path_str,
                            style=text.body_medium(app.theme_mode, color=COLORS["ui"][app.theme_mode.value]["primary"], italic=True)
                        ),
                    ]
                )
                # flet_charts.MatplotlibChart(
                #     figure=mesh_fig,
                #     expand=True,
                # )
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