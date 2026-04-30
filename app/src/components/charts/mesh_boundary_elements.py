import flet as ft
import flet.canvas as cv
import numpy as np

import MecFEM as mf

from ._states import *
from ._data import *
from ._mesh_lines import MeshLinesChart
from ._mesh_nodes import MeshNodesChart

from contexts import *

@ft.component
def MeshBoundaryElementsChart() -> ft.Control:
    def _px_to_data_x(px: float) -> float:
        w = (chart.size["width"] or 1.0) - _pad["left"] - _pad["right"]
        return min_x + ((px - _pad["left"]) / w) * (max_x - min_x)

    def _px_to_data_y(py: float) -> float:
        h = (chart.size["height"] or 1.0) - _pad["top"] - _pad["bottom"]
        return min_y + (1.0 - (py - _pad["top"]) / h) * (max_y - min_y)

    def _draw_rect():
        x0 = min(selection_box.x0, selection_box.x1)
        y0 = min(selection_box.y0, selection_box.y1)
        w = abs(selection_box.x1 - selection_box.x0)
        h = abs(selection_box.y1 - selection_box.y0)

        set_selection_shapes(
            [
                cv.Rect(
                    x=x0, y=y0, width=w, height=h,
                    paint=ft.Paint(
                        color=ft.Colors.with_opacity(0.15, theme.colors["success"]),
                        style=ft.PaintingStyle.FILL,
                    ),
                ),
                cv.Rect(
                    x=x0, y=y0, width=w, height=h,
                    paint=ft.Paint(
                        color=theme.colors["success"],
                        style=ft.PaintingStyle.STROKE,
                        stroke_width=1.5,
                    ),
                ),
            ]
        )

    def _on_tap_down(e: ft.TapEvent):
        x0 = e.local_position.x if e.local_position else 0.0
        y0 = e.local_position.y if e.local_position else 0.0

        print(f"Tap at: ({x0:.1f}, {y0:.1f})")
        selection_box.set_initial_position(x=x0, y=y0)

    def _on_pan_update(e: ft.DragUpdateEvent):
        if e.local_position is None:
            return

        selection_box.update_final_position(
            dx=e.local_delta.x if e.local_delta else 0.0, 
            dy=e.local_delta.y if e.local_delta else 0.0
        )

        _draw_rect()

    def _on_pan_end(e):
        if e.local_position is None:
            return       

        px_x0 = min(selection_box.x0, selection_box.x1)
        px_x1 = max(selection_box.x0, selection_box.x1)
        px_y0 = min(selection_box.y0, selection_box.y1)
        px_y1 = max(selection_box.y0, selection_box.y1)

        x_min = _px_to_data_x(px_x0)
        x_max = _px_to_data_x(px_x1)
        y_min = _px_to_data_y(px_y1)
        y_max = _px_to_data_y(px_y0)

        selected_indices = [
            s.id for s in chart.spots if x_min <= s.x <= x_max and y_min <= s.y <= y_max
        ]

        chart.update_spots_selection(selected_indices)

        set_selection_shapes([])
        selection_box.reset()

    def get_data_bounding_box():
        X = [s.x for s in chart.spots]
        Y = [s.y for s in chart.spots]
        offset = 0.1
        _min_x = float(np.min(X))
        _max_x = float(np.max(X))
        _min_y = float(np.min(Y))
        _max_y = float(np.max(Y))

        _min_x -= offset * abs(_max_x - _min_x)
        _max_x += offset * abs(_max_x - _min_x)
        _min_y -= offset * abs(_max_y - _min_y)
        _max_y += offset * abs(_max_y - _min_y)

        if (_max_x - _min_x) < (_max_y - _min_y):
            max_y = _max_y
            min_y = _min_y
            center_x = 0.5 * (_min_x + _max_x)
            min_x = center_x - 0.5 * (_max_y - _min_y)
            max_x = center_x + 0.5 * (_max_y - _min_y)
        elif (_max_x - _min_x) > (_max_y - _min_y):
            max_x = _max_x
            min_x = _min_x
            center_y = 0.5 * (_min_y + _max_y)
            min_y = center_y - 0.5 * (_max_x - _min_x)
            max_y = center_y + 0.5 * (_max_x - _min_x)
        else:
            max_x = _max_x
            min_x = _min_x
            max_y = _max_y
            min_y = _min_y

        return min_x, max_x, min_y, max_y

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
            [
                [
                    nodes_coords[elem.nodes][node_id, 0], 
                    nodes_coords[elem.nodes][node_id, 1]
                ] for node_id in simulation.state.mesh.get_vertices_ids(elem)
            ] for elem in simulation.state.mesh.elems[simulation.state.mesh.dim - 1]
        ]

        return ChartState(spots=spots, elements=elements, spots_selected=[])
    
    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)
    
    if simulation.state.mesh is None:
        return None

    selection_shapes, set_selection_shapes = ft.use_state([])
    chart, set_chart = ft.use_state(get_chart_data())

    ft.use_effect(lambda: set_chart(get_chart_data()), [chart])

    min_x, max_x, min_y, max_y = get_data_bounding_box()

    selection_box, _ = ft.use_state(SelectionBoxState())
    
    _pad = {
        "left": 0,
        "right": 0,
        "top": 0,
        "bottom": 0,
    }

    return ft.Stack(
        expand=True,
        aspect_ratio=1.0,
        controls=[
            MeshLinesChart(chart, *get_data_bounding_box()),
            MeshNodesChart(chart, *get_data_bounding_box()),
            ft.GestureDetector(
                aspect_ratio=1.0,
                content=cv.Canvas(
                    shapes=selection_shapes, 
                    expand=True,
                    aspect_ratio=1.0,
                ),
                on_tap_down=_on_tap_down,
                on_pan_update=_on_pan_update,
                on_pan_end=_on_pan_end,
                expand=True,
            ),
        ]
    )

