import matplotlib.pyplot as plt
import numpy as np

from .mesh_struct import Mesh
from MecFEM.geometry.isoparametric_elements import ReferenceElements

def plot_mesh(mesh:Mesh, ax:plt.Axes, nodes_ids:bool=False, elems_ids:bool=False, zoom_out:float=0.1) -> plt.Axes:
    """
    Plots the mesh on the given Axes object.

    Parameters
    ----------    
    mesh : Mesh 
        The mesh to plot.
    ax : plt.Axes
        The matplotlib Axes object to plot on.
    nodes_ids : bool, optional
        If True, plot node IDs. Default is False.
    elems_ids : bool, optional
        If True, plot element IDs. Default is False.
    
    Returns:
    -------
    ax : plt.Axes
        The Axes object with the mesh plotted.
    """
    nodes_coords = mesh.get_nodes_coordinates()
    ax.scatter(
        nodes_coords[:, 0], 
        nodes_coords[:, 1],
        color='k',
        marker='o',
        zorder=-10
    )

    for elem in mesh.elems[mesh.dim]:
        elem_coords = nodes_coords[elem.nodes]
        ax.plot(
            elem_coords[:, 0], 
            elem_coords[:, 1], 
            color='k',
            linestyle=None,
            zorder=-10
        )

        vertices_ids = np.arange(ReferenceElements().get_by_type(elem.type).association[0]).tolist()
        vertices_ids.append(vertices_ids[0])  # Close the polygon
        ax.plot(
            elem_coords[vertices_ids, 0], 
            elem_coords[vertices_ids, 1], 
            color='k',
            linestyle='-',
            linewidth=1,
            zorder=-10
        )
    
    if nodes_ids:
        for node in mesh.nodes:
            ax.text(
                node.X[0], 
                node.X[1], 
                f"n{node.id}",
                color='k',
                fontsize=10,
                fontdict={'weight': 'bold'},
                ha='right',
                va='bottom',
                zorder=-10
            )
    if elems_ids:
        for dim in range(mesh.dim+1):
            for elem in mesh.elems[dim]:
                elem_coords = nodes_coords[elem.nodes]
                centroid = np.mean(elem_coords, axis=0)
                ax.text(
                    centroid[0], 
                    centroid[1], 
                    f"e{elem.id}",
                    color='k',
                    fontsize=12,
                    fontdict={'weight': 'bold'},
                    ha='center',
                    va='center',
                    zorder=-10
                )

    min_x, min_y = np.min(nodes_coords[:, 0:mesh.dim], axis=0)
    max_x, max_y = np.max(nodes_coords[:, 0:mesh.dim], axis=0)

    ax.set_xlim(min_x - zoom_out*(max_x - min_x), max_x + zoom_out*(max_x - min_x))
    ax.set_ylim(min_y - zoom_out*(max_y - min_y), max_y + zoom_out*(max_y - min_y))

    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Mesh Plot')
    
    return ax