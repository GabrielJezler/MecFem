import flet as ft
import flet.canvas as cv
import flet_charts as fch
import numpy as np

import MecFEM as mf

from .states import *
from .data import *

from contexts import *

@ft.component
def MeshNodeSelectorChart() -> ft.Control:
    def _on_chart_resize(e):
        _set_widget_size({"w": e.width, "h": e.height})

    def _px_to_data_x(px: float) -> float:
        w = (_widget_size["w"] or 1.0) - _pad["left"] - _pad["right"]
        return min_x + ((px - _pad["left"]) / w) * (max_x - min_x)

    def _px_to_data_y(py: float) -> float:
        h = (_widget_size["h"] or 1.0) - _pad["top"] - _pad["bottom"]
        return min_y + (1.0 - (py - _pad["top"]) / h) * (max_y - min_y)

    def _draw_rect():
        x0 = min(selection_box.x0, selection_box.x1)
        y0 = min(selection_box.y0, selection_box.y1)
        w = abs(selection_box.x1 - selection_box.x0)
        h = abs(selection_box.y1 - selection_box.y0)

        set_rect_shapes(
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
            i for i, s in enumerate(chart.spots)
            if x_min <= s.x <= x_max and y_min <= s.y <= y_max
        ]

        chart.update_selected(selected_indices)

        set_rect_shapes([])
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
            ) for node in simulation.state.mesh.nodes if node.id in nodes_ids
        ]

        return ChartState(spots=spots, selected=[])
    
    theme = ft.use_context(ThemeContext)
    simulation = ft.use_context(SimulationContext)

    if simulation.state.mesh is None:
        return None

    chart, set_chart = ft.use_state(get_chart_data())
    rect_shapes, set_rect_shapes = ft.use_state([])

    ft.use_effect(lambda: set_chart(get_chart_data()), [simulation.state.mesh])

    chart_ref = ft.Ref[fch.ScatterChart]()
    gd_ref = ft.Ref[ft.GestureDetector]()

    nodes_coords = simulation.state.mesh.get_nodes_coordinates()[:, :2]

    min_x, max_x, min_y, max_y = get_data_bounding_box()

    selection_box, set_selection_box = ft.use_state(SelectionBoxState())

    _widget_size, _set_widget_size = ft.use_state({"w": None, "h": None})
    
    _pad = {
        "left": 0,
        "right": 0,
        "top": 0,
        "bottom": 0,
    }

    return ft.Stack(
        expand=True,
        aspect_ratio=1.0,
        data=chart.selected,
        controls=[
            *[
                fch.LineChart(
                    aspect_ratio=1.0,
                    expand=True,
                    tooltip=None,
                    interactive=False,
                    min_x=min_x,
                    max_x=max_x,
                    min_y=min_y,
                    max_y=max_y,
                    left_axis = fch.ChartAxis(show_labels=False, label_size=0),
                    right_axis = fch.ChartAxis(show_labels=False, label_size=0),
                    top_axis = fch.ChartAxis(show_labels=False, label_size=0),
                    bottom_axis = fch.ChartAxis(show_labels=False, label_size=0),
                    data_series=[
                        fch.LineChartData(
                            color=theme.colors["text"],
                            stroke_width=1,
                            points=[
                                fch.LineChartDataPoint(
                                    x=nodes_coords[elem.nodes][node_id, 0],
                                    y=nodes_coords[elem.nodes][node_id, 1],
                                ) for node_id in simulation.state.mesh.get_vertices_ids(elem)
                            ]
                        )
                    ]

                ) for elem in simulation.state.mesh.elems[simulation.state.mesh.dim - 1]
            ],
            fch.ScatterChart(
                aspect_ratio=1.0,
                ref=chart_ref,
                expand=True,
                min_x=min_x,
                max_x=max_x,
                min_y=min_y,
                max_y=max_y,
                left_axis = fch.ChartAxis(show_labels=False, label_size=0),
                right_axis = fch.ChartAxis(show_labels=False, label_size=0),
                top_axis = fch.ChartAxis(show_labels=False, label_size=0),
                bottom_axis = fch.ChartAxis(show_labels=False, label_size=0),
                spots=[
                    fch.ScatterChartSpot(
                        x=s.x,
                        y=s.y,
                        radius=s.radius,
                        color=theme.colors["text"] if i not in chart.selected else theme.colors["primary"],
                    ) for i, s in enumerate(chart.spots)
                ],
                on_size_change=_on_chart_resize,
            ),
            ft.GestureDetector(
                aspect_ratio=1.0,
                ref=gd_ref,
                content=cv.Canvas(
                    shapes=rect_shapes, 
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

