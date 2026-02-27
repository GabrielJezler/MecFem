import numpy as np

from ..geometry.isoparametric_elements import ReferenceElements

class Element:
    """Basic data structure for elements"""
    def __init__(self,id:int,t:int, nodes:list[int]):
        """Create element of label i, type t, with list of nodes n"""
        self._id:int = id
        self._type:int = np.array(t)
        self._nodes:np.ndarray = nodes
        self._dim:int = ReferenceElements().get_by_type(t).dim

    def __eq__(self, value):
        if isinstance(value, self.__class__):
            if self.id == value.id and self.type == value.type and self.nodes == value.nodes:
                return True
        
        return False
    
    def __repr__(self):
        return f"Element(id={self.id}, type={self.type}, nodes={self.nodes})"

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