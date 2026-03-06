import numpy as np
import matplotlib.pyplot as plt
import gmsh
import copy

from ..geometry.isoparametric_elements import ReferenceElements

from .node import Node
from .element import Element

class Mesh:
    """Class containing basic data structure for unstructured mesh"""
    def __init__(self, filename:str, dim:int=2):
        """Create mesh of dimension d"""
        if dim not in [1, 2, 3]:
            raise ValueError("Mesh dimension must be 1, 2 or 3.")
        
        if not filename.endswith('.msh'):
            raise ValueError("Mesh file must be a .msh file.")

        self._filename:str = filename
        self._outfile:str | None = None
        self._dim:int = dim
        self._nodes:list[Node] = []
        self._elems:list[list[Element]] = [[] for _ in range(dim + 1)]

        self.read_gmsh()

    def __repr__(self):
        return f"Mesh(filename={self.filename}, dim={self.dim})"
    
    def __eq__(self, value):
        if isinstance(value, self.__class__):
            if self.n_elements == value.n_elements and self.n_nodes == value.n_nodes:
                for elem_id in range(self.n_elements):
                    if self.elems[self.dim][elem_id] != value.elems[value.dim][elem_id]:
                        return False
                    
                for node_id in range(self.n_nodes):
                    if self.nodes[node_id] != value.nodes[node_id]:
                        return False

                return True

        return False

    @property
    def filename(self):
        return self._filename
    
    @property
    def outfile(self):
        return self._outfile

    @property
    def dim(self):
        return self._dim
    
    @property
    def nodes(self):
        return self._nodes
    
    @property
    def elems(self):
        return self._elems
    
    @property
    def n_nodes(self):
        """Return number of nodes in the mesh"""
        return len(self._nodes)
    
    @property
    def n_elements(self):
        """Return number of elements of the mesh dimension in the mesh"""
        return len(self._elems[self.dim])

    def read_gmsh(self) -> None:
        """
        Reads a .msh file using the gmsh module and creates the Mesh structure.
        
        """
        gmsh.initialize()
        gmsh.open(self._filename)

        node_ids, node_coords, _ = gmsh.model.mesh.getNodes()
        node_coords = np.array(node_coords).reshape(-1, 3)

        self.add_nodes(node_ids - 1, node_coords)  # python is 0-based

        elem_types, elem_tags, elem_node_tags = gmsh.model.mesh.getElements()
        n_elem_types = 0
        for i, elem_type in enumerate(elem_types):
            elem_data = ReferenceElements().get_by_type(elem_type)
            
            elem_tag = elem_tags[i]
            elem_node_tag = elem_node_tags[i] - 1 # python is 0-based

            nodes_per_elem = elem_data.n_nodes
            connectivity = elem_node_tag.reshape(-1, nodes_per_elem) # reshape to (nElements, nodesPerElement)

            self.add_elements(elem_tag - 1, elem_type, connectivity)  # python is 0-based
            
            n_elem_types += 1

        gmsh.finalize()

        if self.n_elements == 0:
            raise ValueError('No elements added to the mesh')

    def get_nodes_coordinates(self):
        """
        Get the coordinates of all nodes in the mesh
        
        Returns:
            np.ndarray: Array of shape (nNodes, 3) containing the coordinates of the nodes
        """
        coords = []
        for node in self._nodes:
            coords.append(node.X)

        return np.array(coords)
    
    def get_elements_cg_coordinates(self, dim:int=None):
        """
        Get the coordinates of the center of gravity of the elements of a specific dimension

        Parameters:
        ----------
        dim: int | None
            The dimension of the elements. If None, use mesh dimension. Defaults to None.

        Returns:
        -------
        np.ndarray: Array of shape (nElements, 3) containing the coordinates of the center of gravity of the elements
        """
        if dim is None:
            dim = self._dim
        
        coords = []
        for elem in self._elems[dim]:
            elem_coords = self.get_nodes_coordinates_by_element(elem.id, dim)
            cg_coords = np.mean(elem_coords, axis=0)
            coords.append(cg_coords)

        return np.array(coords)

    def get_elements_nodal_coordinates(self, dim:int=None):
        """
        Get the coordinates of the nodes of the elements of a specific dimension

        Parameters:
        ----------
        dim: int | None
            The dimension of the elements. If None, use mesh dimension.
            Defaults to None.

        Returns:
        -------
        np.ndarray: List (nElements, nNodesPerElement, 3) containing the coordinates
        of the nodes of the elements. Note that the nNodesPerElement can be different
        for each element, so the list is not a regular array.
        """
        if dim is None:
            dim = self._dim
        
        coords = []
        for elem in self._elems[dim]:
            elem_coords = self.get_nodes_coordinates_by_element(elem.id, dim)
            coords.append(elem_coords)

        return coords

    def get_nodes_coordinates_by_element(self, elem_id:int, dim:int | None=None):
        """
        Get the coordinates of the nodes of a specific element

        Parameters:
        elem_id: int 
            The ID of the element
        dim: int | None 
            The dimension of the element. If None, use mesh dimension. Defaults to None.

        
        Returns:
            np.ndarray: Array of shape (nNodesPerElement, 3) containing the coordinates of the nodes of the element
        """
        if dim is None:
            dim = self._dim
        
        elem = self.get_element_by_id(elem_id, dim)
        coords = []
        for node_id in elem.nodes:
            node = self.get_nodes_by_id(node_id)
            coords.append(node.X)
        
        return np.array(coords)

    def get_nodes_by_id(self, id:int):
        """
        Get a node by its ID

        Parameters:
            id (int): The ID of the node to retrieve
        
        Returns:
            Node: The node with the specified ID
        """
        for node in self._nodes:
            if node.id == id:
                return node
        
        raise ValueError(f"Node with id {id} not found")
    
    def get_element_by_id(self, id:int, dim:int | None = None):
        """
        Get an element by its ID

        Parameters:
        id: int 
            The ID of the element to retrieve
        dim: int | None
            The dimension of the element. If None, use mesh dimension. Defaults to None.

        Returns:
            Element: The element with the specified ID
        """
        if dim is None:
            dim = self._dim

        for elem in self._elems[dim]:
            if elem.id == id:
                return elem
        
        raise ValueError(f"Element with id {id} not found")
    
    def get_elements_by_dim(self, dim:int=None):
        """
        Get all elements of a specific dimension

        Parameters:
        ----------
        dim: int | None
            The dimension of the elements. If None, use mesh dimension. Defaults to None.

        Returns:
        -------
        elems : list[Element]
            List of elements of the specified dimension
        """
        if dim is None:
            dim = self._dim
        
        return self._elems[dim]

    def get_elements_ids(self, dim:int=None):
        """
        Get the IDs of all elements in the mesh

        Parameters:
        ----------
        dim: int | None
            The dimension of the elements. If None, use mesh dimension. Defaults to None.
        
        Returns:
        -------
        ids : np.ndarray
            Array of shape (nElements,) containing the IDs of the elements
        """
        if dim is None:
            dim = self._dim
        
        ids = []
        for elem in self._elems[dim]:
            ids.append(elem.id)
        
        return np.array(ids)

    def get_connectivity_matrix(self, dim:int=None):
        """
        Get the connectivity matrix of the mesh

            [
                [node1_elem1, node2_elem1, ..., nodeN_elem1],

                [node1_elem2, node2_elem2, ..., nodeN_elem2],
                
                ...
                
                [node1_elemM, node2_elemM, ..., nodeN_elemM]
            ]

        Parameters:
        ----------
        dim: int | None
            The dimension of the elements. If None, use mesh dimension. Defaults to None.            

        Returns:
            np.ndarray: Array of shape (nElements, nNodesPerElement) containing the connectivity of the elements
        """
        if dim is None:
            dim = self._dim
        
        connectivity = []
        for elem in self._elems[dim]:
            connectivity.append(elem.nodes)
        
        return connectivity

    def add_node(self,id:int, x:float, y:float=0., z:float=0.):
        """
        Add node with label id and coordinates (x,y,z) to the mesh

        Parameters:
        ----------
        id : int
            The ID of the node
        x : float
            The x-coordinate of the node
        y : float, optional
            The y-coordinate of the node, by default 0.
        z : float, optional
            The z-coordinate of the node, by default 0.
        """
        self.nodes.append(Node(id,x,y,z))

    def add_nodes(self, ids:list[int] | np.ndarray, coords:np.ndarray):
        """
        Add multiple nodes to the mesh
        
        Parameters:
        ids: list[int] 
            List of node IDs
        coords: np.ndarray 
            Array of shape (nNodes, 3) containing the coordinates of the nodes
        """
        for i, node_id in enumerate(ids):
            x, y, z = coords[i]
            self.add_node(node_id, x, y, z)
    
    def add_element(self, id:int, type:int, nodes:list[int]):
        """
        Add element with label id, type, nodes to the mesh
        
        Parameters:
        ----------
        id : int
            The ID of the element
        type : int
            The type tag of the element
        nodes : list[int]
            List of node IDs that make up the element
    """
        dim = ReferenceElements().get_by_type(type).dim
        self._elems[dim].append(Element(id, type, nodes))

    def add_elements(self, ids:list[int] | np.ndarray, type:int, connectivity:np.ndarray):
        """Add multiple elements to the mesh
        
        Parameters:
        ----------
        ids: list[int] 
            List of element IDs
        types: list[int] 
            List of element type tags
        connectivity: np.ndarray 
            Array of shape (nElements, nNodesPerElement) containing the connectivity of the elements
        """
        for i, elem_id in enumerate(ids):
            node_list = connectivity[i].tolist()
            self.add_element(elem_id, type, node_list)

    def plot(self, ax:plt.Axes | None=None, nodes_marker:bool=True, nodes_ids:bool=False, elems_ids:bool=False, zoom_out:float=0.1) -> plt.Axes:
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
        if self.dim == 3:
            raise ValueError("This functions work for 1D or 2D meshes. For 3D use ...")
        
        if ax is None:
            fig, ax = plt.subplots()

        nodes_coords = self.get_nodes_coordinates()
        ax.scatter(
            nodes_coords[:, 0], 
            nodes_coords[:, 1],
            color='k',
            marker='o' if nodes_marker else None,
            s=50 if nodes_marker else 0,
            zorder=-10
        )

        for elem in self._elems[self.dim]:
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
            for node in self._nodes:
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
            for dim in range(self.dim+1):
                for elem in self._elems[dim]:
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

        _min = np.min(nodes_coords[:, 0:self.dim], axis=0)
        _max = np.max(nodes_coords[:, 0:self.dim], axis=0)

        if self.dim == 1:
            ax.set_xlim(_min[0] - zoom_out*(_max[0] - _min[0]), _max[0] + zoom_out*(_max[0] - _min[0]))
        elif self.dim == 2:
            ax.set_xlim(_min[0] - zoom_out*(_max[0] - _min[0]), _max[0] + zoom_out*(_max[0] - _min[0]))
            ax.set_ylim(_min[1] - zoom_out*(_max[1] - _min[1]), _max[1] + zoom_out*(_max[1] - _min[1]))
        else:
            raise ValueError("Only mesh with dimensions 1 or 2 are supported")

        ax.set_aspect('equal')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Mesh Plot')
        
        return ax

    def create_out_file(self) -> None:
        """
        Create an output file for writing results. The output file will have the same name as the input file with "_out.msh" suffix.
        """
        self._outfile = self._filename.replace('.msh', '_out.msh')
        try:
            with open(self._outfile, 'x') as f:
                pass
        except FileExistsError:
            print("File already exists, did not overwrite.")

        gmsh.initialize()
        gmsh.open(self._filename)

        gmsh.write(self._outfile)
        gmsh.finalize()     

    def write_nodal_vector_data(self, values:np.ndarray, times:np.ndarray, label:str) -> None:
        """
        Write nodal vector data to a gmsh file. This can be used to write displacement data for each node.
        The file will be written in the same format as the input mesh file, but with additional views containing the nodal data.
        It will be placed in the same directory as the input mesh file with the name `<input_mesh_name>_out.msh`.

        Parameters
        ----------
        values : np.ndarray
            Array of shape (nSteps, nNodes, nComponents) containing the nodal vector data to write.
        times : np.ndarray
            Array of shape (nSteps,) containing the time values corresponding to each step.
        label : str
            The label for the data in gmsh.
        """
        if times.shape[0] != values.shape[0]:
            raise ValueError(f"Number of time steps does not match number of value sets: expected {values.shape[0]}, got {times.shape[0]}")

        if self.n_nodes != values.shape[1]:
            raise ValueError(f"Number of nodes in mesh does not match number of values: expected {self.n_nodes}, got {values.shape[1]}")
        
        if values.shape[2] not in [1, 2, 3]:
            raise ValueError("Values must be 1D, 2D or 3D.")

        if self._outfile is None:
            self.create_out_file()

        nodes_tags = [node.id + 1 for node in self._nodes]
        vector = copy.deepcopy(values)
        if values.shape[2] != 3:
            vector = np.concatenate((vector, np.zeros((values.shape[0], values.shape[1], 3 - values.shape[2]))), axis=2)

        gmsh.initialize()
        gmsh.open(self._outfile)
        
        print("Nodal views")
        print(gmsh.view.getTags())

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

        gmsh.write(self._outfile)
        gmsh.option.setNumber("PostProcessing.SaveMesh", 0)
        print("Nodal views")
        print(gmsh.view.getTags())
        for view_tag in gmsh.view.getTags():
            gmsh.view.write(view_tag, self._outfile, append=True)
        
        gmsh.finalize()

    def write_element_tensor2_data(self, values:np.ndarray, times:np.ndarray, label:str) -> None:
        """
        Write element tensor data to a gmsh file. This can be used to write stress or strain data for each element.
        The file will be written in the same format as the input mesh file, but with additional views containing the element data.
        It will be placed in the same directory as the input mesh file with the name `<input_mesh_name>_out.msh`.

        Parameters
        ----------
        values : np.ndarray
            Array of shape (nSteps, nElements, 3, 3) containing the element tensor data to write.
        times : np.ndarray
            Array of shape (nSteps,) containing the time values corresponding to each step.
        label : str
            The label for the data in gmsh.
        """
        if times.shape[0] != values.shape[0]:
            raise ValueError(f"Number of time steps does not match number of value sets: expected {values.shape[0]}, got {times.shape[0]}")

        if self.n_elements != values.shape[1]:
            raise ValueError(f"Number of elements in mesh does not match number of values: expected {self.n_elements}, got {values.shape[1]}")
        
        if values.shape[2] not in [1, 2, 3]:
            raise ValueError("Values must be 1D, 2D or 3D.")
        
        if self._outfile is None:
            self.create_out_file()

        elements_tags = [elem.id + 1 for elem in self._elems[self.dim]]
        tensor = np.zeros((values.shape[0], values.shape[1], 3, 3))
        tensor[:, :, :values.shape[2], :values.shape[3]] = values

        gmsh.initialize()
        gmsh.open(self._outfile)
        
        print("Element views")
        print(gmsh.view.getTags())

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

        gmsh.write(self._outfile)
        gmsh.option.setNumber("PostProcessing.SaveMesh", 0)
        print("Element views")
        print(gmsh.view.getTags())
        for view_tag in gmsh.view.getTags():
            gmsh.view.write(view_tag, self._outfile, append=True)

        gmsh.finalize()
