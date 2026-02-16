import numpy as np
import os
import copy
import gmsh

# import MecFEM as mf
# from MecFEM.model import NonLinearFE
from .mesh_struct import Mesh


def element_tensor2_data(meshfile:str, outfile:str, mesh:Mesh, values:np.ndarray, times:np.ndarray, label:str) -> None:
    """
    Write node vector data to a gmsh file. This can be used to write displacement data for each node.

    Parameters
    ----------
    meshfile : str
        Path to the gmsh file where the node data will be written.
    outfile : str
        Path to the output gmsh file where the element data will be written.
    mesh : Mesh
        The mesh object containing the elements.
    values : ndarray
        Array of values to be written for each element. Shape should be (n_steps, n_elements, dim, dim).
    times : ndarray
        Array of times corresponding to each set of values. Shape should be (n_steps,).
    label : str
        Label for the data being written. This will be used in the gmsh file to identify the data.

    Returns
    -------
    None

    """
    if times.shape[0] != values.shape[0]:
        raise ValueError(f"Number of time steps does not match number of value sets: expected {values.shape[0]}, got {times.shape[0]}")

    if mesh.n_elements != values.shape[1]:
        raise ValueError(f"Number of elements in mesh does not match number of values: expected {mesh.n_elements}, got {values.shape[1]}")
    
    if values.shape[2] not in [1, 2, 3]:
        raise ValueError("Values must be 1D, 2D or 3D.")

    elements_tags = [elem.id + 1 for elem in mesh.elems[mesh.dim]]
    tensor = np.zeros((values.shape[0], values.shape[1], 3, 3))
    tensor[:, :, :values.shape[2], :values.shape[3]] = values

    gmsh.initialize()
    gmsh.open(meshfile)

    view = gmsh.view.add(label)

    for i in range(values.shape[0]):
        data = np.column_stack([
            tensor[i,:,0,0],
            tensor[i,:,0,1],
            tensor[i,:,0,2],
            tensor[i,:,1,0],
            tensor[i,:,1,1],
            tensor[i,:,1,2],
            tensor[i,:,2,0],
            tensor[i,:,2,1],
            tensor[i,:,2,2]
        ])
        
        gmsh.view.addModelData(
            tag=view,
            step=i,
            modelName=gmsh.model.getCurrent(),
            dataType="ElementData",
            tags=elements_tags,
            data=data,
            time=times[i],
            numComponents=9
        )

    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)

    gmsh.write(outfile)
    gmsh.option.setNumber("PostProcessing.SaveMesh", 0)
    for view_tag in gmsh.view.getTags():
        gmsh.view.write(view_tag, outfile, append=True)

    gmsh.finalize()



def node_vector_data(meshfile:str, outfile:str, mesh:Mesh, values:np.ndarray, times:np.ndarray, label:str) -> None:
    """
    Write node vector data to a gmsh file. This can be used to write displacement data for each node.

    Parameters
    ----------
    meshfile : str
        Path to the gmsh file where the node data will be written.
    outfile : str
        Path to the output gmsh file where the node data will be written.
    mesh : Mesh
        The mesh object containing the nodes.
    values : ndarray
        Array of values to be written for each node. Shape should be (n_steps, n_nodes, dim).
    times : ndarray
        Array of times corresponding to each set of values. Shape should be (n_steps,).
    label : str
        Label for the data being written. This will be used in the gmsh file to identify the data.

    Returns
    -------
    None

    """
    if times.shape[0] != values.shape[0]:
        raise ValueError(f"Number of time steps does not match number of value sets: expected {values.shape[0]}, got {times.shape[0]}")

    if mesh.n_nodes != values.shape[1]:
        raise ValueError(f"Number of nodes in mesh does not match number of values: expected {mesh.n_nodes}, got {values.shape[1]}")
    
    if values.shape[2] not in [1, 2, 3]:
        raise ValueError("Values must be 1D, 2D or 3D.")

    nodes_tags = [node.id + 1 for node in mesh.nodes]
    vector = copy.deepcopy(values)
    if values.shape[2] != 3:
        vector = np.concatenate((vector, np.zeros((values.shape[0], values.shape[1], 3 - values.shape[2]))), axis=2)

    gmsh.initialize()
    gmsh.open(meshfile)

    view = gmsh.view.add(label)

    for i in range(values.shape[0]):
        gmsh.view.addModelData(
            tag=view,
            step=i,
            modelName=gmsh.model.getCurrent(),
            dataType="NodeData",
            tags=nodes_tags,
            data=vector[i,:,:],
            time=times[i],
            numComponents=3
        )

    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)

    gmsh.write(outfile)
    gmsh.option.setNumber("PostProcessing.SaveMesh", 0)
    for view_tag in gmsh.view.getTags():
        gmsh.view.write(view_tag, outfile, append=True)
    
    gmsh.finalize()


                