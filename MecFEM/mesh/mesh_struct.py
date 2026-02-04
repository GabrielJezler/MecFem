import numpy as np

from ..geometry.isoparametric_elements import ReferenceElements

class Node:
    """Basic data structure for nodes"""
    def __init__(self,i:int, x:float,y:float,z:float):
        """Create node of label i and coordinates (x,y,z)"""
        self._id = i
        self._X = [x, y, z]

    @property
    def id(self):
        return self._id
    
    @property
    def X(self):
        return self._X
        

class Element:
    """Basic data structure for elements"""
    def __init__(self,id:int,t:int, nodes:list[int]):
        """Create element of label i, type t, with list of nodes n"""
        self._id:int = id
        self._type:int = t
        self._nodes:np.ndarray = nodes
        self._dim:int = ReferenceElements().get_by_type(t).dim

    @property
    def id(self):
        return self._id
    
    @property
    def type(self):
        return self._type
    
    @property
    def nodes(self):
        return self._nodes
    
    @property
    def dim(self):
        return self._dim
    
    @property
    def n_nodes(self):
        """Return number of nodes of the element"""
        return len(self._nodes)
    
    def element_data(self):
        """Return GmshElementData instance for the element type"""
        gmsh_elems = ReferenceElements()
        return gmsh_elems.get_by_type(self._type)
    
    def print_element_data(self):
        """Print element data"""
        print(self.element_data())


class Mesh:
    """Class containing basic data structure for unstructured mesh"""
    def __init__(self,dim:int=2):
        """Create mesh of dimension d"""
        self._dim:int = dim
        self._nodes:list[Node] = []
        self._elems:list[list[Element]] = [[] for _ in range(dim + 1)]

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
        """Return number of elements in the mesh"""
        return len(self._elems)
    
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
    
    def get_nodes_coodinates_by_element(self, elem_id:int, dim:int | None=None):
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
    
    def get_element_by_id(self, id:int, dim:int=None):
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
