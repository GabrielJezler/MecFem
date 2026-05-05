import flet as ft

from structures.contexts import ThemeContext, SimulationContext
from structures.chart import ChartData, SpotData, ElementData

from ._mesh_lines import MeshLinesChart
from ._mesh_nodes import MeshNodesChart
from ._utils import get_data_bounding_box

@ft.component
def MeshChart() -> ft.Control:
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
            elements=elements
        )

    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    chart, set_chart = ft.use_state(get_chart_data())
 
    ft.use_effect(lambda: set_chart(get_chart_data()), [simulation.state.mesh, theme])

    return ft.Stack(
        expand=True,
        aspect_ratio=1.0,
        controls=[
            MeshNodesChart(chart, *get_data_bounding_box(chart)),
            MeshLinesChart(chart, *get_data_bounding_box(chart))
        ]
    )
