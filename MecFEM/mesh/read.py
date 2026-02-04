import gmsh
import numpy as np
from .mesh_struct import Mesh
from ..geometry.isoparametric_elements import ReferenceElements

def read_gmsh_mesh(filename, dim=1):
    """Reads a .msh file using the gmsh module and creates the Mesh structure"""
    gmsh.initialize()
    gmsh.open(filename)
    mesh = Mesh(dim=dim)
    
    # Read nodes
    node_ids, node_coords, _ = gmsh.model.mesh.getNodes()
    node_coords = np.array(node_coords).reshape(-1, 3)
    
    mesh.add_nodes(node_ids - 1, node_coords)  # python is 0-based

    # Read elements
    elem_types, elem_tags, elem_node_tags = gmsh.model.mesh.getElements()
    n_elem_types = 0
    for i, elem_type in enumerate(elem_types):
        elem_data = ReferenceElements().get_by_type(elem_type)
        # if elem_data.dim == dim: # Get only the elements of the specified dimension
        elem_tag = elem_tags[i]
        elem_node_tag = elem_node_tags[i] - 1 # python is 0-based

        nodes_per_elem = elem_data.n_nodes
        connectivity = elem_node_tag.reshape(-1, nodes_per_elem) # reshape to (nElements, nodesPerElement)

        mesh.add_elements(elem_tag - 1, elem_type, connectivity)  # python is 0-based
        
        n_elem_types += 1
    
    if n_elem_types == 0:
        raise TypeError(f'No elements of dimension {dim} found in the mesh file {filename}')
    if n_elem_types > 1:
        print(f'Warning: More than one element type of dimension {dim} found in the mesh file {filename}. All have been added to the mesh.')

    gmsh.finalize()

    if mesh.n_elements > 0:
        return mesh
    else:
        raise TypeError('No elements added to the mesh')
