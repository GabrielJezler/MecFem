import flet as ft
import flet_charts as fch

from structures.contexts import ThemeContext
from structures.chart import ChartData

@ ft.component
def mesh_lines_chart(chart: ChartData, min_x: float, max_x: float, min_y: float, max_y: float):
    def _on_chart_resize(e):
        chart.update_size(width=e.width, height=e.height)

    theme = ft.use_context(ThemeContext)

    return fch.LineChart(
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
                        x=coords[0],
                        y=coords[1],
                    ) for coords in elem
                ]
            ) for elem in chart.elements
        ],
        on_size_change=_on_chart_resize,
    )

MeshLinesChart = ft.memo(mesh_lines_chart)
