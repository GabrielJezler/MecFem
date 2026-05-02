import numpy as np

from structures.chart import ChartData

def get_data_bounding_box(chart: ChartData):
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
