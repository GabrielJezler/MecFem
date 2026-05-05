import flet as ft
import flet.canvas as cv
import numpy as np

import MecFEM as mf

from structures.contexts import ThemeContext, SimulationContext, SelectorContext
from structures.chart import ChartData, SpotData, ElementData, MeshSelectionZone, MeshSelectionObject
from structures.enums import MeshSelectionObject

from ._mesh_lines import MeshLinesChart
from ._mesh_nodes import MeshNodesChart
from ._mesh_gesture_detetor import MeshGestureDetector
from ._utils import get_data_bounding_box

@ft.component
def MeshSelectorChart() -> ft.Control:
    def _on_chart_resize(e):
        _set_size({"width": e.width, "height": e.height})
        chart.update_size(width=e.width, height=e.height)

    def get_chart_data():
        nodes_coords = simulation.state.mesh.get_nodes_coordinates()[:, :2]

        if selector.zone == MeshSelectionZone.BOUNDARY:
            dim = simulation.state.mesh.dim - 1
        elif selector.zone == MeshSelectionZone.VOLUME:
            dim = simulation.state.mesh.dim

        if selector.object == MeshSelectionObject.NODES:
            nodes_ids = []
            for elem in simulation.state.mesh.elems[dim]:
                nodes_ids.extend(elem.nodes)
            nodes_ids = np.unique(nodes_ids)
        elif selector.object == MeshSelectionObject.ELEMENTS:
            nodes_ids = np.arange(len(simulation.state.mesh.nodes))
        else:
            raise ValueError(f"Invalid selection object: {selector.object}")

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
                vertices=[
                    (
                        nodes_coords[elem.nodes][node_id, 0], 
                        nodes_coords[elem.nodes][node_id, 1]
                    ) for node_id in simulation.state.mesh.get_vertices_ids(elem)
                ],
                color=theme.colors["text"],
                selected_color=theme.colors["primary"],
                id=elem.id
            ) for elem in simulation.state.mesh.elems[dim]
        ]

        return ChartData(
            spots=spots, 
            elements=elements, 
            selection_object=selector.object,
            selection_zone=selector.zone,
            size=_size
        )
    
    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)
    selector = ft.use_context(SelectorContext)

    _size, _set_size = ft.use_state({"width": 1.0, "height": 1.0})
    
    if simulation.state.mesh is None:
        return None

    chart, set_chart = ft.use_state(get_chart_data())

    ft.use_effect(lambda: set_chart(get_chart_data()), [chart, selector, theme])

    if selector.object == MeshSelectionObject.ELEMENTS:
        return ft.Stack(
            expand=True,
            aspect_ratio=1.0,
            controls=[
                MeshLinesChart(chart, *get_data_bounding_box(chart)),
                MeshGestureDetector(chart, *get_data_bounding_box(chart))
            ],
            on_size_change=lambda e: _on_chart_resize(e)
        )
    elif selector.object == MeshSelectionObject.NODES:
        return ft.Stack(
            expand=True,
            aspect_ratio=1.0,
            controls=[
                MeshLinesChart(chart, *get_data_bounding_box(chart)),
                MeshNodesChart(chart, *get_data_bounding_box(chart)),
                MeshGestureDetector(chart, *get_data_bounding_box(chart))
            ],
            on_size_change=lambda e: _on_chart_resize(e)
        )
