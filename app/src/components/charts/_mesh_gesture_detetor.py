import flet as ft
import flet.canvas as cv
import numpy as np

from structures.contexts import ThemeContext, SelectionDataContext
from structures.enums import GestureSelectionMode
from structures.chart import ChartData, RetangularSelectionData, LassoSelectionData

@ft.component
def MeshGestureDetector(
    chart: ChartData,
    min_x: float = 0.0, 
    max_x: float = 1.0, 
    min_y: float = 0.0, 
    max_y: float = 1.0,
):
    def _px_to_data_x(px: np.ndarray | float) -> np.ndarray | float:
        w = (chart.size["width"] or 1.0)
        return min_x + ((px) / w) * (max_x - min_x)

    def _px_to_data_y(py: np.ndarray | float) -> np.ndarray | float:
        h = (chart.size["height"] or 1.0)
        return min_y + (1.0 - (py) / h) * (max_y - min_y)

    def _on_tap_down(e: ft.TapEvent):
        if selection_data is None:
            return

        x0 = e.local_position.x if e.local_position else 0.0
        y0 = e.local_position.y if e.local_position else 0.0

        selection_data.set_initial_position(x=x0, y=y0)

    def _on_pan_update(e: ft.DragUpdateEvent):
        if e.local_position is None or selection_data is None:
            return
        
        selection_data.update_final_position(
            dx=e.local_delta.x if e.local_delta else 0.0, 
            dy=e.local_delta.y if e.local_delta else 0.0
        )

        set_selection_shapes(selection_data.get_shapes(color=theme.colors["success"]))

    def _on_pan_end(e: ft.DragUpdateEvent):
        if e.local_position is None or selection_data is None:
            return

        selected_indices = selection_data.get_selected_indices(
            chart=chart, 
            px_to_data_x_func=lambda p: _px_to_data_x(p), 
            px_to_data_y_func=lambda p: _px_to_data_y(p)
        )
        chart.update_selection(selected_indices)

        set_selection_shapes([])
        selection_data.reset()

    theme = ft.use_context(ThemeContext)
    selection_data = ft.use_context(SelectionDataContext)

    selection_shapes, set_selection_shapes = ft.use_state([])

    return ft.GestureDetector(
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
    )
