import flet as ft
import flet.canvas as cv
import numpy as np

import MecFEM as mf

from ._states import *
from ._data import *
from ._mesh_lines import MeshLinesChart

from contexts import *

@ft.component
def MeshVolumeElementsChart() -> ft.Control:
    def _px_to_data_x(px: float) -> float:
        print('entering _px_to_data_x')
        w = (chart.size["width"] or 1.0) - _pad["left"] - _pad["right"]
        print(f"Widget width: {chart.size['width']}, w: {w}, px: {px}")
        return min_x + ((px - _pad["left"]) / w) * (max_x - min_x)

    def _px_to_data_y(py: float) -> float:
        print('entering _px_to_data_y')
        h = (chart.size["height"] or 1.0) - _pad["top"] - _pad["bottom"]
        print(f"Widget height: {chart.size['height']}, h: {h}, py: {py}")
        return min_y + (1.0 - (py - _pad["top"]) / h) * (max_y - min_y)
    
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
            [
                [
                    nodes_coords[elem.nodes][node_id, 0], 
                    nodes_coords[elem.nodes][node_id, 1]
                ] for node_id in simulation.state.mesh.get_vertices_ids(elem)
            ] for elem in simulation.state.mesh.elems[simulation.state.mesh.dim]
        ]
        # print(ChartState(spots=spots, elements=elements))
        return ChartState(spots=spots, elements=elements)

    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    if simulation.state.mesh is None:
        return None

    chart, set_chart = ft.use_state(get_chart_data())

    ft.use_effect(lambda: set_chart(get_chart_data()), [simulation.state.mesh])

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
            ft.Container() # Delete later
            # ft.GestureDetector(
            #     aspect_ratio=1.0,
            #     ref=gd_ref,
            #     content=cv.Canvas(
            #         shapes=rect_shapes, 
            #         expand=True,
            #         aspect_ratio=1.0,
            #     ),
            #     on_tap_down=_on_tap_down,
            #     on_pan_update=_on_pan_update,
            #     on_pan_end=_on_pan_end,
            #     expand=True,
            # ),
        ]
    )

