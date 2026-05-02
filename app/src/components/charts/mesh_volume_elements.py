import flet as ft
import numpy as np

from structures.contexts import ThemeContext, SimulationContext
from structures.chart import ChartData, SpotData, ElementData
from structures.enums import MeshSelectionMode

from ._mesh_lines import MeshLinesChart
from ._mesh_gesture_detetor import MeshGestureDetector
from ._utils import get_data_bounding_box

@ft.component
def MeshVolumeElementsChart() -> ft.Control:
    def get_chart_data():
        nodes_coords = simulation.state.mesh.get_nodes_coordinates()[:, :2]

        spots = [
            SpotData(
                x=node.X[0],
                y=node.X[1],
                radius=4.0,
                color=theme.colors["text"],
                selected_color=theme.colors["primary"],
                id=node.id
            ) for node in simulation.state.mesh.nodes
        ]
        elements = [
            ElementData(
                vertices=[
                    (
                        nodes_coords[elem.nodes][node_id, 0], 
                        nodes_coords[elem.nodes][node_id, 1]
                    ) for node_id in simulation.state.mesh.get_vertices_ids(elem)
                ],
                color=theme.colors["text"],
                selected_color=theme.colors["primary"],
                id=elem.id
            ) for elem in simulation.state.mesh.elems[simulation.state.mesh.dim]
        ]

        return ChartData(
            spots=spots, 
            elements=elements,
            selection_mode=MeshSelectionMode.ELEMENTS
        )

    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    if simulation.state.mesh is None:
        return None

    chart, set_chart = ft.use_state(get_chart_data())

    ft.use_effect(lambda: set_chart(get_chart_data()), [chart]) # mesh

    return ft.Stack(
        expand=True,
        aspect_ratio=1.0,
        controls=[
            MeshLinesChart(chart, *get_data_bounding_box(chart)),
            MeshGestureDetector(chart, *get_data_bounding_box(chart))
        ]
    )

