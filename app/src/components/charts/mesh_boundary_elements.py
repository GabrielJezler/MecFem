import flet as ft
import flet.canvas as cv
import numpy as np

import MecFEM as mf

from structures.contexts import ThemeContext, SimulationContext
from structures.chart import ChartData, SpotData, ElementData
from structures.enums import MeshSelectionMode

from ._mesh_lines import MeshLinesChart
from ._mesh_nodes import MeshNodesChart
from ._mesh_gesture_detetor import MeshGestureDetector
from ._utils import get_data_bounding_box

@ft.component
def MeshBoundaryElementsChart() -> ft.Control:
    def get_chart_data():
        nodes_coords = simulation.state.mesh.get_nodes_coordinates()[:, :2]

        nodes_ids = []
        for elem in simulation.state.mesh.elems[simulation.state.mesh.dim - 1]:
            nodes_ids.extend(elem.nodes)
        nodes_ids = np.unique(nodes_ids)

        spots = [
            SpotData(
                x=node.X[0],
                y=node.X[1],
                radius=4.0,
                color=theme.colors["text"],
                selected_color=theme.colors["primary"],
                id=node.id
            ) for node in simulation.state.mesh.nodes if (node.id in nodes_ids)
        ]

        elements = [
            ElementData(
                # vertices=np.array(
                #     [
                #         [
                #             nodes_coords[elem.nodes][node_id, 0], 
                #             nodes_coords[elem.nodes][node_id, 1]
                #         ] for node_id in simulation.state.mesh.get_vertices_ids(elem)
                #     ]
                # ),
                vertices=[
                    (
                        nodes_coords[elem.nodes][node_id, 0], 
                        nodes_coords[elem.nodes][node_id, 1]
                    ) for node_id in simulation.state.mesh.get_vertices_ids(elem)
                ],
                color=theme.colors["text"],
                selected_color=theme.colors["primary"],
                id=elem.id
            ) for elem in simulation.state.mesh.elems[simulation.state.mesh.dim - 1]
        ]

        return ChartData(
            spots=spots, 
            elements=elements, 
            selection_mode=MeshSelectionMode.NODES
        )
    
    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)
    
    if simulation.state.mesh is None:
        return None

    chart, set_chart = ft.use_state(get_chart_data())

    ft.use_effect(lambda: set_chart(get_chart_data()), [chart])

    return ft.Stack(
        expand=True,
        aspect_ratio=1.0,
        controls=[
            MeshLinesChart(chart, *get_data_bounding_box(chart)),
            MeshNodesChart(chart, *get_data_bounding_box(chart)),
            MeshGestureDetector(chart, *get_data_bounding_box(chart))
        ]
    )
