import flet as ft
import flet.canvas as cv
import flet_charts as fch
import numpy as np

import MecFEM as mf

from .states import *
from .data import *

from contexts import *

@ft.component
def MeshChart(mesh: mf.mesh.Mesh | None) -> ft.Control:
    if mesh is None:
        return ft.Container()
    
    nodes_coords = mesh.get_nodes_coordinates()[:, :2]

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
        spots = [
            SpotData(
                x=node.X[0],
                y=node.X[1],
                radius=4.0,
                color=theme.colors["text"],
                selected_color=theme.colors["primary"],
                id=node.id
            ) for node in mesh.nodes
        ]
        return ChartState(spots=spots, selected=[])
    
    theme = ft.use_context(ThemeContext)

    chart, set_chart = ft.use_state(get_chart_data())

    ft.use_effect(lambda: set_chart(get_chart_data()), [mesh])

    chart_ref = ft.Ref[fch.ScatterChart]()

    min_x, max_x, min_y, max_y = get_data_bounding_box()

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
                                ) for node_id in mesh.get_vertices_ids(elem)
                            ]
                        )
                    ]

                ) for elem in mesh.elems[mesh.dim]
            ],
            fch.ScatterChart(
                aspect_ratio=1.0,
                ref=chart_ref,
                expand=True,
                interactive=True,
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
                        color=theme.colors["text"],
                        tooltip=f"id:{s.id}" if s.id is not None else None,
                    ) for s in chart.spots
                ],
            )
        ]
    )

