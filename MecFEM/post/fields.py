import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np

from MecFEM.model import NonLinearFEModel
from MecFEM.utils.stress import von_mises

def plot_2d_arrows(x_nodes, F_nodes: np.ndarray, ax=None, label:str='Field', color:str='C0'):
    """
    Plots the Field vectors on the mesh.

    Parameters
    ----------
    model : NonLinearFEModel
        The finite element model.
    U : ndarray
        The Field vector at each node. Shape should be (n_nodes, dim).
    ax : matplotlib.axes.Axes, optional
        The axes on which to plot. If None, a new figure and axes are created.
    label : str, optional
        Label for the arrows. Default is 'Field'.
    color : str, optional
        Color for the arrows. Default is 'C0'.
        
    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes with the Field plot.
    """
    if ax is None:
        fig, ax = plt.subplots()

    ax.quiver(
        x_nodes[:, 0],
        x_nodes[:, 1],
        F_nodes[:, 0],
        F_nodes[:, 1],
        color=color,
        angles='xy',
        scale_units='width',
        label=label
    )

    return ax

def plot_2d_field(x_nodes: np.ndarray, F_nodes: np.ndarray, component: str="Mag", ax=None, label:str='Field Magnitude'):
    """
    Plots the magnitude of the Field field on the mesh.

    Parameters
    ----------
    x_nodes : np.ndarray
        Coordinates of the nodes. Shape should be (n_nodes, dim).
    F_nodes : ndarray
        The Field vector at each node. Shape should be (n_nodes, dim).
    component : str, optional
        The component of the Field to plot. Options are:
            - "Mag": Magnitude of the Field vector.
            - "X": X-component of the Field vector.
            - "Y": Y-component of the Field vector.
        Default is "Mag".    
    ax : matplotlib.axes.Axes, optional
        The axes on which to plot. If None, a new figure and axes are created.
    label : str, optional
        Label for the colorbar. Default is 'Field Magnitude'.    

    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes with the Field plot.
    """
    if ax is None:
        fig, ax = plt.subplots()
    
    min_x, min_y = np.min(x_nodes, axis=0)
    max_x, max_y = np.max(x_nodes, axis=0)

    if component == "Mag":
        z = np.linalg.norm(F_nodes, axis=1)
    elif component == "X":
        z = F_nodes[:, 0]
    elif component == "Y":
        z = F_nodes[:, 1]
    elif component == "VM":
        z = von_mises(F_nodes)
    else:
        raise ValueError(f"Unknown component '{component}'. Valid options are 'Mag', 'X', 'Y', 'VM'.")
    
    max_z = np.max(z)
    min_z = np.min(z)

    cont = ax.tricontourf(
        x_nodes[:, 0],
        x_nodes[:, 1],
        z,
        cmap='plasma',
        levels=50,
        vmin=min_z,
        vmax=max_z,
        zorder=-100
    )

    cbar = plt.colorbar(cont, ax=ax, label=f'{label} - {component}', ticks=np.linspace(min_z, max_z, 11))
    cbar.ax.set_ylim(min_z, max_z)
    cbar.formatter.set_useMathText(True)

    ax.set_aspect('equal')
    ax.set_title(f'{label} - {component}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    return ax
