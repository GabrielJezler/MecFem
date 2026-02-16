import matplotlib.pyplot as plt
import numpy as np

from .mesh_struct import Mesh
from MecFEM.geometry.isoparametric_elements import ReferenceElements

def plot_mesh(mesh:Mesh, ax:plt.Axes | None=None, nodes_marker:bool=True, nodes_ids:bool=False, elems_ids:bool=False, zoom_out:float=0.1) -> plt.Axes:
    """
    Plots the mesh on the given Axes object.

    Parameters
    ----------    
    mesh : Mesh 
        The mesh to plot.
    ax : plt.Axes
        The matplotlib Axes object to plot on.
    nodes_marker : bool, optional
        If True, plot nodes as markers. Default is True.
    nodes_ids : bool, optional
        If True, plot node IDs. Default is False.
    elems_ids : bool, optional
        If True, plot element IDs. Default is False.
    
    Returns:
    -------
    ax : plt.Axes
        The Axes object with the mesh plotted.
    """
    if mesh.dim == 3:
        raise ValueError("This functions work for 1D or 2D meshes. For 3D use ...")
    
    if ax is None:
        fig, ax = plt.subplots()

    nodes_coords = mesh.get_nodes_coordinates()
    ax.scatter(
        nodes_coords[:, 0], 
        nodes_coords[:, 1],
        color='k',
        marker='o' if nodes_marker else None,
        s=50 if nodes_marker else 0,
        zorder=-10
    )

    for elem in mesh.elems[mesh.dim]:
        elem_coords = nodes_coords[elem.nodes]

        vertices_ids = np.arange(ReferenceElements().get_by_type(elem.type).association[0]).tolist()
        vertices_ids.append(vertices_ids[0])  # Close the polygon
        ax.plot(
            elem_coords[vertices_ids, 0], 
            elem_coords[vertices_ids, 1], 
            color='k',
            linestyle='-',
            linewidth=2,
            zorder=-12
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
                zorder=-9
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
                    zorder=-5 - dim
                )

    _min = np.min(nodes_coords[:, 0:mesh.dim], axis=0)
    _max = np.max(nodes_coords[:, 0:mesh.dim], axis=0)

    if mesh.dim == 1:
        ax.set_xlim(_min[0] - zoom_out*(_max[0] - _min[0]), _max[0] + zoom_out*(_max[0] - _min[0]))
    elif mesh.dim == 2:
        ax.set_xlim(_min[0] - zoom_out*(_max[0] - _min[0]), _max[0] + zoom_out*(_max[0] - _min[0]))
        ax.set_ylim(_min[1] - zoom_out*(_max[1] - _min[1]), _max[1] + zoom_out*(_max[1] - _min[1]))
    else:
        raise ValueError("Only mesh with dimensions 1 or 2 are supported")

    ax.set_aspect('equal')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Mesh Plot')
    
    return ax