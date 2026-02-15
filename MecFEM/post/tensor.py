import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.collections import PolyCollection
import matplotlib.cm as cm
import numpy as np

from MecFEM.model import NonLinearFE
from MecFEM.utils.stress import von_mises

def plot_2d_field(model: NonLinearFE, F: np.ndarray, component: str="vm", ax=None, label:str='Stress'):
    """
    Plots the magnitude of a tensor field on the mesh. This field is element-wise, so the values are defined at the center of each element.

    Parameters
    ----------
    model : NonLinearFEModel
        The finite element model.
    F : ndarray
        The tensor field vector at each node. Shape should be (n_elem, dim, dim).
    component : str, optional
        The component of the Field to plot. Options are:
            - "xx": XX-component of the field tensor.
            - "yy": YY-component of the field tensor.
            - "xy": XY-component of the field tensor.
            - "vm": Von Mises stress of the field tensor.
        Default is "vm".    
    ax : matplotlib.axes.Axes, optional
        The axes on which to plot. If None, a new figure and axes are created.
    label : str, optional
        Label for the colorbar. Default is 'Stress'.    

    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes with the Field plot.
    """
    if ax is None:
        fig, ax = plt.subplots()

    elif component.lower() == "xx":
        z = F[:, 0, 0]
    elif component.lower() == "yy":
        z = F[:, 1, 1]
    elif component.lower() == "xy":
        z = F[:, 0, 1]
    elif component.lower() == "vm":
        z = von_mises(F)
    else:
        raise ValueError(f"Unknown component '{component}'. Valid options are 'xx', 'yy', 'xy', 'vm'.")

    x_nodes = model.get_nodes_coordinates()

    polygons = [x_nodes[nodes] for nodes in model.connect]

    collection = PolyCollection(polygons, array=z, cmap='plasma', zorder=-100)
    ax.add_collection(collection)

    cbar = plt.colorbar(collection, ax=ax, label=f'{label} - {component}', ticks=np.linspace(np.min(z), np.max(z), 11))
    cbar.ax.set_ylim(np.min(z), np.max(z))
    cbar.formatter.set_useMathText(True)

    ax.set_aspect('equal')
    ax.set_title(f'{label} - {component}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    return ax