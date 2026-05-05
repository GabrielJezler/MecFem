import flet as ft
import flet_charts as fch

from structures.contexts import ThemeContext
from structures.chart import ChartData

@ ft.component
def mesh_nodes_chart(chart: ChartData, min_x: float, max_x: float, min_y: float, max_y: float):
    theme = ft.use_context(ThemeContext)
    
    return fch.ScatterChart(
        aspect_ratio=1.0,
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
                x=spot.x,
                y=spot.y,
                radius=spot.radius,
                color=theme.colors["text"] if not spot.id in chart.spots_selected else theme.colors["primary"],
                tooltip=f"id:{spot.id}" if spot.id is not None else None,
            ) for spot in chart.spots
        ],
    )

MeshNodesChart = ft.memo(mesh_nodes_chart)
