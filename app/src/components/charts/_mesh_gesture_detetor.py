import flet as ft
import flet.canvas as cv
import numpy as np
import asyncio

from components import Tooltip
from structures.contexts import ThemeContext, SelectorContext
from structures.chart import ChartData

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
        if selector.mode is None:
            return

        x0 = e.local_position.x if e.local_position else 0.0
        y0 = e.local_position.y if e.local_position else 0.0

        selector.mode.set_initial_position(x=x0, y=y0)

    def _on_pan_update(e: ft.DragUpdateEvent):
        if e.local_position is None or selector.mode is None:
            return
        
        selector.mode.update_final_position(
            dx=e.local_delta.x if e.local_delta else 0.0, 
            dy=e.local_delta.y if e.local_delta else 0.0
        )

        set_selection_shapes(selector.mode.get_shapes(color=theme.colors["success"]))

    def _on_pan_end(e: ft.DragUpdateEvent):
        if e.local_position is None or selector.mode is None:
            return

        selected_indices = selector.mode.get_selected_indices(
            chart=chart, 
            px_to_data_x_func=lambda p: _px_to_data_x(p), 
            px_to_data_y_func=lambda p: _px_to_data_y(p)
        )
        chart.update_selection(selected_indices, extend_selection=ctrl_hold)

        set_selection_shapes([])
        selector.mode.reset()

    def handle_reset(e: ft.ControlEvent):
        chart.update_selection([], extend_selection=False)
        set_selection_shapes([])
        selector.mode.reset()

    async def on_ctrl_event_down(e: ft.ControlEvent):
        if e.key.lower().startswith("control"):
            set_ctrl_hold(True)
    
    async def on_ctrl_event_up(e: ft.ControlEvent):
        if e.key.lower().startswith("control"):
            set_ctrl_hold(False)

    theme = ft.use_context(ThemeContext)
    selector = ft.use_context(SelectorContext)

    selection_shapes, set_selection_shapes = ft.use_state([])
    ctrl_hold, set_ctrl_hold = ft.use_state(False)

    # keyboard_listener = 

    # ft.use_effect(lambda: asyncio.create_task(keyboard_listener.focus()), [selector])

    # Fix ctrl hold
    return ft.GestureDetector(
        expand=True,
        aspect_ratio=1.0,
        content=ft.KeyboardListener(
            expand=True,
            autofocus=True,
            content=ft.Stack(
                expand=True,
                aspect_ratio=1.0,
                controls=[
                    cv.Canvas(
                        shapes=selection_shapes,
                        expand=True,
                        aspect_ratio=1.0,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.FloatingActionButton(
                                icon=ft.Icon(
                                    ft.CupertinoIcons.CLEAR_CIRCLED,
                                    color=theme.colors["text"],
                                ),
                                bgcolor=theme.colors["bg_01"],
                                margin=4,
                                mini=True,
                                shape=ft.RoundedRectangleBorder(radius=16),
                                tooltip=Tooltip(
                                    message="Clear selection",
                                    wait_duration=ft.Duration(seconds=1),
                                ),
                                on_click=lambda e: handle_reset(e),
                            ),
                            ft.FloatingActionButton(
                                icon=ft.Icon(
                                    ft.CupertinoIcons.ADD_CIRCLED,
                                    color=theme.colors["text"],
                                ),
                                bgcolor=theme.colors["bg_01"],
                                margin=4,
                                mini=True,
                                shape=ft.RoundedRectangleBorder(radius=16),
                                tooltip=Tooltip(
                                    message="Add boundary condition",
                                    wait_duration=ft.Duration(seconds=1),
                                ),
                                # on_click=lambda e: handle_reset(e),
                            ),
                        ]
                    )
                ]
            ),
            on_key_down=lambda e: asyncio.create_task(on_ctrl_event_down(e)),
            on_key_up=lambda e: asyncio.create_task(on_ctrl_event_up(e)),
        ),
        on_tap_down=_on_tap_down,
        on_pan_update=_on_pan_update,
        on_pan_end=_on_pan_end,
        on_enter=lambda e: asyncio.create_task(e.control.content.focus()),
    )
