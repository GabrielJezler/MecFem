import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import matplotlib.cm as cm
import numpy as np

from MecFEM.model import NonLinearFE

def plot_2d_arrows(model, F_nodes: np.ndarray, ax=None, scale:float=1.0, label:str='Field'):
    """
    Plots the Field vectors on the mesh.

    Parameters
    ----------
    model : NonLinearFEModel
        The finite element model.
    F_nodes : ndarray
        The Field vector at each node. Shape should be (n_nodes, dim).
    ax : matplotlib.axes.Axes, optional
        The axes on which to plot. If None, a new figure and axes are created.
    scale : float, optional
        Scaling factor for the arrows. Default is 1.0.
    label : str, optional
        Label for the arrows. Default is 'Field'.
        
    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes with the Field plot.
    """
    if ax is None:
        fig, ax = plt.subplots()

    x_nodes = model.get_nodes_coordinates()

    qv = ax.quiver(
        x_nodes[:, 0],
        x_nodes[:, 1],
        F_nodes[:, 0],
        F_nodes[:, 1],
        np.linalg.norm(F_nodes, axis=1),
        angles='xy',
        scale=scale,
        scale_units='width',
        label=label,
        cmap='plasma',
    )

    cbar = plt.colorbar(qv, ax=ax, label=f'{label} Magnitude')

    ax.set_aspect('equal')
    ax.set_title(label)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    return ax

def plot_2d_field(model: NonLinearFE, F_nodes: np.ndarray, component: str="Mag", ax=None, label:str='Field Magnitude'):
    """
    Plots the magnitude of the Field field on the mesh.

    Parameters
    ----------
    model : NonLinearFEModel
        The finite element model.
    F_nodes : ndarray
        The Field vector at each node. Shape should be (n_nodes, dim).
    component : str, optional
        The component of the Field to plot. Options are:
            - "mag": Magnitude of the Field vector.
            - "x": X-component of the Field vector.
            - "y": Y-component of the Field vector.
        Default is "mag".    
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

    if component.lower() == "mag":
        z = np.linalg.norm(F_nodes, axis=1)
    elif component.lower() == "x":
        z = F_nodes[:, 0]
    elif component.lower() == "y":
        z = F_nodes[:, 1]
    else:
        raise ValueError(f"Unknown component '{component}'. Valid options are 'Mag', 'X', 'Y', 'VM'.")
    
    max_z = np.max(z)
    min_z = np.min(z)
    
    X_nodes = model.get_nodes_coordinates()

    for nodes_id in model.connect:
        x_nodes = X_nodes[nodes_id]
        z_nodes = z[nodes_id]

        cont = ax.tricontourf(
            x_nodes[:, 0],
            x_nodes[:, 1],
            z_nodes,
            cmap='plasma',
            levels=50,
            vmin=min_z,
            vmax=max_z,
            zorder=-100
        )

    cbar = plt.colorbar(cm.ScalarMappable(cmap='plasma', norm=plt.Normalize(vmin=min_z, vmax=max_z)), ax=ax, label=f'{label} - {component}', ticks=np.linspace(min_z, max_z, 11))
    cbar.ax.set_ylim(min_z, max_z)
    cbar.formatter.set_useMathText(True)

    ax.set_aspect('equal')
    ax.set_title(f'{label} - {component}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    return ax
