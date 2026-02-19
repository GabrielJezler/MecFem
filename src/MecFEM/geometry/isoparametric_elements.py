import numpy as np

from . import shape_functions as sf
from . import integration as it

class ReferenceElementData:
    """
    Class containing data for a Gmsh element type

    Attributes
    ----------
    type : int
        Gmsh element type number
    name : str
        Name of the element. It serves as a description
    nodes : np.ndarray
        Coordinates of the nodes in the reference element
    n_nodes : int
        Number of nodes of the element
    dim : int
        Dimension of the element
    shape_function : shape function class
        Object for the shape functions of the element
    integration_points : integration points class
        Object for the integration points of the element
    association : list[int]
        Number of nodes associated to vertices, edges, faces, volumes respectively
    order : int
        Polynomial order of the element
    complete : bool
        Whether the element is complete or not
    """
    def __init__(self, type:int, name:str, nodes:np.ndarray, shape_function_class, integration_points_class, association:list[int], interpolation_order:int=1, complete:bool=True):
        self.type = type
        self.name = name

        self.nodes = nodes
        self.n_nodes = nodes.shape[0]
        self.dim = nodes.shape[1]

        self.shape_function = shape_function_class()
        self.integration_points = integration_points_class()

        self.association = association
        self.interpolation_order = interpolation_order
        self.complete = complete
    
    def __repr__(self):
        return f"GmshElementData({self.name})"
    
    def set_integration_number(self, N:int):
        """
        Set number of integration points
        
        Parameters
        ----------
        N : int
            Number of integration points.
        """
        self.integration_points = self.integration_points.__class__(N=N)

class ReferenceElements:
    """
    Class containing Gmsh elements data
    
    All higher order elements are included, both complete and incomplete for 1D and 2D elements.
    For 3D elements, only linear elements are included for now.
    """
    ELEMS = [
        ReferenceElementData(
            type=15, 
            name="point",
            nodes=np.array([[0.0]]), 
            shape_function_class=sf.LagrangePoint,
            integration_points_class=it.GaussPoint,
            association=[1, 0, 0, 0]
        ),
        ReferenceElementData(
            type=1, 
            name="2-node line",
            nodes=np.array([
                [-1.0], [1.0]
            ]),
            shape_function_class=sf.LagrangeLine2,
            integration_points_class=it.GaussLine,
            association=[2, 0, 0, 0]
        ),
        ReferenceElementData(
            type=8, 
            name="3-node second order line", 
            nodes=np.array([
                [-1.0], [1.0], 
                [0.0]
            ]),
            shape_function_class=sf.LagrangeLine3,
            integration_points_class=it.GaussLine,
            association=[2, 1, 0, 0], 
            interpolation_order=2
        ),
        ReferenceElementData(
            type=26, 
            name="4-node third order line", 
            nodes=np.array([
                [-1.0], [1.0], 
                [-1/3], [1/3]
            ]),
            shape_function_class=sf.LagrangeLine4,
            integration_points_class=it.GaussLine,
            association=[2, 2, 0, 0], 
            interpolation_order=3
        ),
        ReferenceElementData(
            type=27, 
            name="5-node fourth order line",
            nodes=np.array([
                [-1.0], [1.0], 
                [-0.5], [0.0], [0.5]
            ]),
            shape_function_class=sf.LagrangeLine5,
            integration_points_class=it.GaussLine,
            association=[2, 3, 0, 0], 
            interpolation_order=4
        ),
        ReferenceElementData(
            type=28, 
            name="6-node fifth order line", 
            nodes=np.array([
                [-1.0], [1.0], 
                [-0.6], [-0.2], [0.2], [0.6]
            ]),
            shape_function_class=sf.LagrangeLine6,
            integration_points_class=it.GaussLine,
            association=[2, 4, 0, 0], 
            interpolation_order=5
        ),
        ReferenceElementData(
            type=3, 
            name="4-node quadrangle", 
            nodes=np.array([
                [-1.0, -1.0], [1.0, -1.0], [1.0, 1.0], [-1.0, 1.0]
            ]),
            shape_function_class=sf.LagrangeQuad4,
            integration_points_class=it.GaussQuadrangle,
            association=[4, 0, 0, 0]
        ),
        ReferenceElementData(
            type=10, 
            name="9-node second order quadrangle",
            nodes=np.array([
                [-1.0, -1.0], [1.0, -1.0], [1.0, 1.0], [-1.0, 1.0],
                [0.0, -1.0], [1.0, 0.0], [0.0, 1.0], [-1.0, 0.0],
                [0.0, 0.0]
            ]),
            shape_function_class=sf.LagrangeQuad9,
            integration_points_class=it.GaussQuadrangle,
            association=[4, 4, 1, 0], 
            interpolation_order=2
        ),
        ReferenceElementData(
            type=16, 
            name="8-node second order incomplete quadrangle", 
            nodes=np.array([
                [-1.0, -1.0], [1.0, -1.0], [1.0, 1.0], [-1.0, 1.0],
                [0.0, -1.0], [1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]
            ]),
            shape_function_class=sf.LagrangeQuad8,
            integration_points_class=it.GaussQuadrangle,
            association=[4, 4, 0, 0], 
            interpolation_order=2, 
            complete=False
        ),
        ReferenceElementData(
            type=2, 
            name="3-node triangle", 
            nodes=np.array([
                [0.0, 0.0], [1.0, 0.0], [0.0, 1.0]
            ]),
            shape_function_class=sf.LagrangeTri3,
            integration_points_class=it.GaussTriangle,
            association=[3, 0, 0, 0]
        ),
        ReferenceElementData(
            type=9, 
            name="6-node second order triangle",
            nodes=np.array([
                [0.0, 0.0], [1.0, 0.0], [0.0, 1.0],
                [0.5, 0.0], [0.5, 0.5], [0.0, 0.5]
            ]),
            shape_function_class=sf.LagrangeTri6,
            integration_points_class=it.GaussTriangle,
            association=[3, 3, 0, 0], 
            interpolation_order=2
        ),
        # ReferenceElementData(
        #     type=20, 
        #     name="9-node third order incomplete triangle", 
        #     nodes=np.array([
        #         [0.0, 0.0], [1.0, 0.0], [0.0, 1.0],
        #         [1/3, 0.0], [2/3, 0.0], [2/3, 1/3], [1/3, 2/3], [0.0, 2/3], [0.0, 1/3]
        #     ]),
        #     shape_function_class=sf.LagrangeTri9,
        #     integration_points_class=None,  # To be implemented
        #     association=[3, 6, 0, 0], 
        #     interpolation_order=2,
        #     complete=False
        # ),
        ReferenceElementData(
            type=21, 
            name="10-node third order triangle",
            nodes=np.array([
                [0.0, 0.0], [1.0, 0.0], [0.0, 1.0],
                [1/3, 0.0], [2/3, 0.0], [2/3, 1/3], [1/3, 2/3], [0.0, 2/3], [0.0, 1/3],
                [1/3, 1/3]
            ]),
            shape_function_class=sf.LagrangeTri10,
            integration_points_class=it.GaussTriangle,
            association=[3, 6, 1, 0], 
            interpolation_order=3
        ),
        # GmshElementData(
        #     type=22, 
        #     name="12-node fourth order incomplete triangle",
        #     nodes=np.array([
        #         [0.0, 0.0], [1.0, 0.0], [0.0, 1.0],
        #         [0.25, 0.0], [0.5, 0.0], [0.75, 0.0], [0.75, 0.25], [0.5, 0.5], [0.25, 0.75], [0.0, 0.75], [0.0, 0.5], [0.0, 0.25]
        #     ]),
        #     shape_function_class=None,  # To be implemented
        #     integration_points_class=None,  # To be implemented
        #     association=[3, 9, 0, 0], 
        #     interpolation_order=4
        # ),
        # GmshElementData(
        #     type=23, 
        #     name="15-node fourth order triangle",
        #     nodes=np.array([
        #         [0.0, 0.0], [1.0, 0.0], [0.0, 1.0],
        #         [0.25, 0.0], [0.5, 0.0], [0.75, 0.0], [0.75, 0.25], [0.5, 0.5], [0.25, 0.75], [0.0, 0.75], [0.0, 0.5], [0.0, 0.25],
        #         [0.25, 0.25], [0.5, 0.25], [0.25, 0.5]
        #     ]),
        #     shape_function_class=None,  # To be implemented
        #     integration_points_class=None,  # To be implemented
        #     association=[3, 9, 3, 0], 
        #     interpolation_order=4
        # ),
        # GmshElementData(
        #     type=24, 
        #     name="15-node fifth order incomplete triangle",
        #     nodes=np.array([
        #         [0.0, 0.0], [1.0, 0.0], [0.0, 1.0],
        #         [0.2, 0.0], [0.4, 0.0], [0.6, 0.0], [0.8, 0.0], [0.8, 0.2], [0.6, 0.4], [0.4, 0.6], [0.2, 0.8], [0.0, 0.8], [0.0, 0.6], [0.0, 0.4], [0.0, 0.2]
        #     ]),
        #     shape_function_class=None,  # To be implemented
        #     integration_points_class=None,  # To be implemented
        #     association=[3, 12, 0, 0], 
        #     interpolation_order=5
        # ),
        # GmshElementData(
        #     type=25, 
        #     name="21-node fifth order triangle",
        #     nodes=np.array([
        #         [0.0, 0.0], [1.0, 0.0], [0.0, 1.0],
        #         [0.2, 0.0], [0.4, 0.0], [0.6, 0.0], [0.8, 0.0], [0.8, 0.2], [0.6, 0.4], [0.4, 0.6], [0.2, 0.8], [0.0, 0.8], [0.0, 0.6], [0.0, 0.4], [0.0, 0.2],
        #         [0.2, 0.2], [0.4, 0.2], [0.6, 0.2], [0.4, 0.4], [0.2, 0.6], [0.2, 0.4]
        #     ]), # Verify order of nodes in face
        #     shape_function_class=None,  # To be implemented
        #     integration_points_class=None,  # To be implemented
        #     association=[3, 12, 6, 0], 
        #     interpolation_order=5
        # ),
        ReferenceElementData(
            type=4, 
            name="4-node tetrahedron",
            nodes=np.array([
                [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]
            ]),
            shape_function_class=sf.LagrangeTet4,
            integration_points_class=it.GaussTetrahedron,
            association=[4, 0, 0, 0]
        ),
        ReferenceElementData(
            type=5, 
            name="8-node hexahedron",
            nodes=np.array([
                [-1.0, -1.0, -1.0], [1.0, -1.0, -1.0], [1.0, 1.0, -1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0], [1.0, -1.0, 1.0], [1.0, 1.0, 1.0], [-1.0, 1.0, 1.0]
            ]),
            shape_function_class=sf.LagrangeHex8,
            integration_points_class=it.GaussHexahedron,
            association=[8, 0, 0, 0]
        ),
        ReferenceElementData(
            type=6, 
            name="6-node prism",
            nodes=np.array([
                [0.0, 0.0, -1.0], [1.0, 0.0, -1.0], [0.0, 1.0, -1.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0]
            ]),
            shape_function_class=sf.LagrangePrism6,
            integration_points_class=it.GaussPrism,
            association=[6, 0, 0, 0]
        ),
        ReferenceElementData(
            type=7, 
            name="5-node pyramid",
            nodes=np.array([
                [-1.0, -1.0, 0.0], [1.0, -1.0, 0.0], [1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [0.0, 0.0, 1.0]
            ]),
            shape_function_class=sf.LagrangePyram5,
            integration_points_class=it.GaussPyramid,
            association=[5, 0, 0, 0]
        ),
    ]

    def get_by_type(self, type:int) -> ReferenceElementData:
        """Return GmshElementData instance for given type"""
        for elem in self.ELEMS:
            if elem.type == type:
                return elem
        raise ValueError(f"Gmsh element with type {type} not found")
    
    