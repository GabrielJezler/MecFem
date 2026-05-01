from dataclasses import dataclass, field
import flet as ft
import flet.canvas as cv
import numpy as np

@dataclass
class SpotData:
    x: float
    y: float
    color: ft.Colors | str
    selected_color: ft.Colors |str
    radius: float = 8.0
    id: int | None = None

@ft.observable
@dataclass
class ChartData:
    spots_selected: list[int] = field(default_factory=list)
    spots: list[SpotData] = field(default_factory=list)
    elements_selected: list[int] = field(default_factory=list)
    elements: list[list[float]] = field(default_factory=list)
    size:dict[str, float] = field(default_factory=lambda: {"width": 1.0, "height": 1.0})

    def update_size(self, width: float, height: float):
        self.size["width"] = width
        self.size["height"] = height

    def update_spots_selection(self, indices: list[int]):
        self.spots_selected = indices

    def update_elements_selection(self, indices: list[int]):
        self.elements_selected = indices

@ft.observable
@dataclass
class RetangularSelectionData:
    points: np.ndarray | None = None

    def set_initial_position(self, x: float, y: float):
        self.points = np.array([[x, y], [x, y]])
    
    def update_final_position(self, dx: float, dy: float):
        if self.points is not None:
            self.points[1,:] = self.points[1,:] + np.array([dx, dy])

    def get_selected_indices(self, chart: ChartData, px_to_data_x_func, px_to_data_y_func):
        if self.points is None:
            return []
        
        min_x = px_to_data_x_func(np.min(self.points[:, 0]))
        max_x = px_to_data_x_func(np.max(self.points[:, 0]))
        min_y = px_to_data_y_func(np.max(self.points[:, 1]))
        max_y = px_to_data_y_func(np.min(self.points[:, 1]))

        return [
            s.id for s in chart.spots if s.id is not None and min_x <= s.x <= max_x and min_y <= s.y <= max_y
        ]
    
    def get_shapes(self, color:str):
        if self.points is None:
            return []

        x0, y0 = self.points[0]
        x1, y1 = self.points[1]
        w = x1 - x0
        h = y1 - y0

        return [
            cv.Rect(
                x=x0, y=y0, width=w, height=h,
                paint=ft.Paint(
                    color=ft.Colors.with_opacity(0.15, color),
                    style=ft.PaintingStyle.FILL,
                ),
            ),
            cv.Rect(
                x=x0, y=y0, width=w, height=h,
                paint=ft.Paint(
                    color=color,
                    style=ft.PaintingStyle.STROKE,
                    stroke_width=1.5,
                ),
            ),
        ]

    def reset(self):
        self.points = None

@ft.observable
@dataclass
class LassoSelectionData:
    points: np.ndarray | None = None

    def set_initial_position(self, x: float, y: float):
        self.points = np.array([[x, y]])
    
    def update_final_position(self, dx: float, dy: float):
        if self.points is not None:
            x, y = self.points[-1]
            self.points = np.vstack([self.points, [x + dx, y + dy]])

    def get_selected_indices(self, chart: ChartData, px_to_data_x_func, px_to_data_y_func):
        if self.points is None:
            return []

        from matplotlib.path import Path

        spots_points = np.array([[s.x, s.y] for s in chart.spots])
        lasso_points = np.array([[px_to_data_x_func(p[0]), px_to_data_y_func(p[1])] for p in self.points])
        
        path = Path(lasso_points)
        inside = path.contains_points(spots_points)

        return [s.id for s, is_inside in zip(chart.spots, inside) if (s.id is not None and is_inside)]

    def get_shapes(self, color:str):
        if self.points is None:
            return []
        
        elements = [
            cv.Path.MoveTo(x=p[0], y=p[1]) if i == 0 else cv.Path.LineTo(x=p[0], y=p[1])
            for i, p in enumerate(self.points)
        ]

        return [
            cv.Path(
                elements=elements,
                paint=ft.Paint(
                    color=ft.Colors.with_opacity(0.15, color),
                    style=ft.PaintingStyle.FILL,
                ),
            ),
            cv.Path(
                elements=elements,
                paint=ft.Paint(
                    color=color,
                    style=ft.PaintingStyle.STROKE,
                    stroke_width=1.5,
                ),
            ),
        ]

    def reset(self):
        self.points = None

@ft.observable
@dataclass
class SelectionData:
    method: RetangularSelectionData | LassoSelectionData | None = None

