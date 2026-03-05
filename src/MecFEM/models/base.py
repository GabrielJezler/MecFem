import matplotlib.pyplot as plt
import numpy as np
import copy
import gmsh

from ..mesh import Mesh
from ..elements import NonLinearFiniteElement, LinearFiniteElement
from ..boundary_conditions import BCStep

class Base:
    """
    Data structure for non linear FE model
    
    Attributes:
        - material: Material object defining the constitutive behavior
        - mesh: Mesh object defining the geometry and discretization of the problem
        - dim: mesh dimension
        - n_nodes: number of nodes
        - connect: table of connectivity (list of lists)

            Example: 
            
                connect=[
                    [node1_elem1, node2_elem1, ..., nodeN_elem1],

                    [node1_elem2, node2_elem2, ..., nodeN_elem2],
                    
                    ...
                    
                    [node1_elemM, node2_elemM, ..., nodeN_elemM]
                ]

        - n_dofs: number of degrees of freedom (n_nodes * dim)
        - free_dofs: array of free degrees of freedom
        - fixed_dofs: array of fixed degrees of freedom
        - elems: list of NonLinearFiniteElement objects representing the elements in the mesh
        - boundary_elems: list of NonLinearFiniteElement objects representing the boundary elements in the mesh
        - U: array of nodal displacements at each time step (shape: (n_time_steps, n_nodes, dim))
        - T: array of time steps corresponding to the nodal displacements (shape: (n_time_steps,))
    """
    def __init__(self, mesh: Mesh, material, element_type) -> None:
        if element_type not in [LinearFiniteElement, NonLinearFiniteElement]:
            raise ValueError(f"element_type must be either LinearFiniteElement or NonLinearFiniteElement, got {element_type}")

        self.material = material
        self.mesh = mesh

        self.dim: int = mesh.dim
        self.n_nodes: int = mesh.n_nodes
        self.connect: np.array = mesh.get_connectivity_matrix()

        self.n_dofs = self.n_nodes * self.dim
        self.free_dofs = np.arange(self.n_dofs).astype(int)
        self.fixed_dofs = np.array([], dtype=int)

        self.elems: list[LinearFiniteElement | NonLinearFiniteElement] = []
        self.boundary_elems: list[LinearFiniteElement | NonLinearFiniteElement] = []

        for elem in mesh.elems[self.dim]:
            x_nodes = mesh.get_nodes_coordinates_by_element(elem.id, self.dim)
            self.elems.append(element_type(elem, x_nodes))

        for elem in mesh.elems[self.dim - 1]:
            x_nodes = mesh.get_nodes_coordinates_by_element(elem.id, self.dim - 1)
            self.boundary_elems.append(element_type(elem, x_nodes))
        
        self._volumetric_force_steps: list[(np.ndarray, BCStep)] = []
        self._external_forces_steps: list[(np.ndarray, BCStep)] = []
        self._displacement_steps: list[(np.ndarray, BCStep)] = []

        self.U:np.ndarray | None = None # Displacement
        self.T:np.ndarray | None = None # Time steps

    def __repr__(self):
        return f"{self.__class__.__name__}(n_nodes: {self.n_nodes}, n_elems: {self.n_elements}, dim: {self.dim}, material: {self.material})"
    
    def __eq__(self, value):
        if isinstance(value, self.__class__):
            if self.mesh == value.mesh and self.material == value.material:
                return True

        return False
    
    @property
    def n_elements(self):
        """Get number of elements"""
        return len(self.elems)
    
    def get_nodes_coordinates(self) -> np.ndarray:
        """
        Get coordinates of all nodes in the mesh.

        Returns
        -------
        x_nodes : ndarray
            Coordinates of all nodes. This is an array of shape (n_nodes, dim).

        """
        x_nodes = np.zeros((self.n_nodes, self.dim))
        for e, elem in enumerate(self.elems):
            for i, node_id in enumerate(self.connect[e]):
                x_nodes[node_id, :] = elem.x_nodes[i, 0:elem.dim]

        return x_nodes
    
    def add_displacement_bc(self, dofs: np.ndarray, step: BCStep) -> None:
        """
        Add displacement boundary conditions to the model.

        Parameters
        ----------
        dofs : ndarray
            Array of degrees of freedom (DOFs) where the displacement is applied. This is an array of shape (n_dofs,).
        step : BCStep
            Boundary condition step defining the time-dependent values for the DOFs.

        Returns
        -------
        None.

        """
        if not isinstance(step, BCStep):
            raise TypeError("step must be an instance of BCStep")
        
        dofs = dofs.astype(int)
        if np.any(np.isin(dofs, self.fixed_dofs)):
            mask = np.isin(dofs, self.fixed_dofs)
            raise ValueError(f"The following DOFs are already fixed: {dofs[mask]}. It can only be fixed to the model once.")

        self.fixed_dofs = np.concatenate((self.fixed_dofs, dofs))
        self.free_dofs = np.setdiff1d(self.free_dofs, self.fixed_dofs)

        self._displacement_steps.append((dofs, step))
        return None

    def add_volumetric_force(self, step: BCStep, elems_id: np.ndarray | None = None) -> None:
        """
        Add volumetric force to the model.

        Parameters
        ----------
        elems_id : ndarray | None
            Array of element ids where the volumetric force is applied.  If None then
            all elements are considered to have the volumetric force applied. This is
            an array of shape (n_elems_id,). Pay attention that the element ids are the
            one given by the mesh and not simply the order they appear in `self.elems`.
        step : BCStep
            Boundary condition step defining the time-dependent values for the DOFs.

        Returns
        -------
        None.

        """
        if isinstance(step, BCStep):
            if elems_id is None:
                elems_id = np.array([elem.id for elem in self.elems])
            
            self._volumetric_force_steps.append((elems_id, step))
        else:
            raise TypeError("step must be an instance of BCStep")
        
        return None
    
    def add_external_force(self, elems_id: np.ndarray, step: BCStep) -> None:
        """
        Add external force to the model.

        Parameters
        ----------
        elems_id : ndarray
            Array of element ids where the external force is applied (they are elements
            of dimention `self.dim -1`). 
            This is an array of shape (n_elems_id,). 
            Pay attention that the element ids are the one given by the mesh and not
            simply the order they appear in `self.elems`.
        step : BCStep
            Boundary condition step defining the time-dependent values for the DOFs.

        Returns
        -------
        None.
        """
        if isinstance(step, BCStep):
            self._external_forces_steps.append((elems_id, step))
        else:
            raise TypeError("step must be an instance of BCStep")
        
        return None
 
    def plot_bc(self, ax: plt.Axes=None, time:float=1.0) -> None:
        if ax is None:
            fig, ax = plt.subplots()

        X_nodes = self.get_nodes_coordinates()
        c = 1
        for dofs, step in self._displacement_steps:
            nodes_id = np.unique(dofs // self.dim)
            axis = np.unique(dofs % self.dim)
            
            label = f"Displacement {c} "
            U = np.zeros(len(nodes_id))
            V = np.zeros(len(nodes_id))
            for a in axis:
                if a not in [0, 1, 2]:
                    raise ValueError("Invalid axis value. Axis must be 0, 1 or 2.")
                
                if a == 0:
                    U = U + step.interp(time)(X_nodes[nodes_id, :])
                elif a == 1:
                    V = V +  step.interp(time)(X_nodes[nodes_id, :])

            ax.scatter(X_nodes[nodes_id, 0], X_nodes[nodes_id, 1], c=f"C{c-1}", label=label, s=20, zorder=0)

            ax.quiver(X_nodes[nodes_id, 0], X_nodes[nodes_id, 1], U, V, color=f"C{c-1}",zorder=-20)

            c += 1

        c = 1
        for elems_id, step in self._volumetric_force_steps:
            label = f"Volumetric Force {c}"
            X_cg = np.zeros((len(elems_id), self.dim))
            F = np.zeros((len(elems_id), self.dim))
            for i, elem_id in enumerate(elems_id):
                elem = self.mesh.get_element_by_id(elem_id)
                X_cg[i, :] = np.mean(self.mesh.get_nodes_coordinates_by_element(elem_id)[:, :self.dim], axis=0)
                F[i, :] = step.interp(time)._field(X_cg[i, :][np.newaxis, :])[0, :]

            ax.scatter(X_cg[:, 0], X_cg[:, 1], c=f"C{c-1}", marker="x", label=label, s=40, zorder=0)
            ax.quiver(X_cg[:, 0], X_cg[:, 1], F[:, 0], F[:, 1], color=f"C{c-1}", zorder=-20)
            c += 1

        ax.set_title(f"Boundary conditions at t = {time:.4f}")
        return None

    def extract(self, U: np.ndarray, elem_id: int) -> np.ndarray:
        """
        extract nodal values of field U for element e

        Parameters
        ----------
        U : 2-entry array
            nodal displacement field.
        elem_id : int
            element id.

        Returns
        -------
        uNod : 2-entry array
            nodal values of displacement field for element e.

        """
        nodes_id = self.connect[elem_id]
        uNod = []
        for i in nodes_id:
            uNod.append(U[i])
            
        return np.array(uNod)

    def assemble(self,elem_id: int, vNod: np.ndarray, V: np.ndarray) -> None:
        """
        Assemble nodal values for ndim-entry array:
            add nodal values for element e to global array V

        Parameters
        ----------
        elem_id : int
            Element id.
        vNod :  ndarray
            Nodal values for element elem_id.
        V : ndarray
            All nodal values of the mesh.
        
        Returns
        -------
        None.

        """
        iNod = self.connect[elem_id]
        V[np.ix_(*([iNod, range(self.dim)] * (V.ndim // 2)))] += vNod
        return None

    def update_elements(self, U: np.ndarray) -> None:
        """
        Update all elements based on nodal displacements and material properties.

        Parameters
        ----------
        U : ndarray
            Nodal displacement field. This is an array of shape (n_nodes, dim).

        Returns
        -------
        None.

        """
        for e in range(self.n_elements):
            u_node = self.extract(U, e)
            self.elems[e].update(self.material, u_node)
        
        return None

    def get_volumetric_forces_steps(self, elem_id: int):
        """
        Get the Volumetric forces steps for a certain element

        Parameters:
        -----------
        elem_id : int
            Element id from mesh.
        """
        steps = []
        for ids, step in self._volumetric_force_steps:
            if elem_id in ids:
                steps.append(step)

        return steps

    def volumetric_forces(self, t: float=0.0) -> np.ndarray:
        """
        Compute global volumetric force vector.

        Parameters
        ----------
        t : float
            Current time.

        Returns
        -------
        Fvol : ndarray
            Global volumetric force vector. This is an array of shape (n_nodes, dim).

        """
        Fvol = np.zeros((self.n_nodes, self.dim))

        if len(self._volumetric_force_steps) == 0:
            return Fvol
        
        for i, elem in enumerate(self.elems):
            steps = self.get_volumetric_forces_steps(elem.id)
            if steps == []:
                continue

            volumetric_forces_elem = np.sum([step.interp(t)(elem.x_nodes[:, 0:elem.dim], elem.fshape()) for step in steps], axis=0)

            self.assemble(i, elem.volumetric_force(volumetric_forces_elem), Fvol)

        return Fvol
    
    def external_forces(self, t: float=0.0) -> np.ndarray:
        """
        Compute global external force vector.

        Parameters
        ----------
        t : float
            Current time.

        Returns
        -------
        Fext : ndarray
            Global external force vector. This is an array of shape (n_nodes, dim).

        """
        Fext = np.zeros((self.n_nodes, self.dim))

        if self._external_forces_steps == []:
            return Fext

        for i, elem in enumerate(self.elems):
            external_forces_elem = np.sum(np.array([f(elem.x_nodes[:, 0:elem.dim], elem.fshape) for f in self._external_forces_steps]), axis=0)

            self.assemble(i, elem.external_force(external_forces_elem), Fext)

        return Fext
    
    def apply_displacement(self, U: np.ndarray, t: float=0.0) -> np.ndarray:
        """
        Apply displacement boundary conditions to the nodal displacement field U.

        Parameters
        ----------
        U : ndarray
            Nodal displacement field. This is an array of shape (n_dofs).
        t : float
            Current time.

        Returns
        -------
        U_bc : ndarray
            Nodal displacement field with boundary conditions applied. This is an array of shape (n_dofs,).

        """
        U_bc = copy.deepcopy(U)
        nodes_coords = self.get_nodes_coordinates()

        for dofs, step in self._displacement_steps:
            U_bc[np.ix_(dofs)] = step.interp(t)(nodes_coords[dofs // self.dim, :])
        
        return U_bc

    def sigma(self, averaged=True) -> np.ndarray:
        """
        Get Cauchy stress for each element.

        Parameters
        ----------
        averaged : bool, optional
            If True, return averaged stress at nodes. If False, return stress at integration points. The default is True.

        Returns
        -------
        sigma : ndarray
            Cauchy stress at element. This is an array of shape (n_elems, dim, dim).

        """
        if self.U is None or self.T is None:
            raise ValueError("No solution found. Please run the solver first.")
        
        if not averaged:
            raise ValueError("Non averaged values are not yet available.")
        
        sigma = np.zeros((self.T.shape[0], len(self.elems), self.dim, self.dim))

        for step in range(self.T.shape[0]):
            for e, elem in enumerate(self.elems):
                u_nodes = self.extract(self.U[step, :], e)
                sigma_elem = elem.sigma(u_nodes, self.material)

                sigma[step, e, :, :] = np.mean(sigma_elem, axis=0)

        return sigma
    
    def load_gmsh_results(self, filename: str, U_values_name: str) -> None:
        """
        Load results from a Gmsh .pos file.

        Parameters
        ----------
        filename : str
            Path to the .pos file containing the results.
        U_values_name : str


        Returns
        -------
        None.

        """
        gmsh.initialize()
        gmsh.open(filename)

        print("--- Loading results from Gmsh ---")
        print(f"--- Filename: {filename}")

        view_tag = None
        for tag in gmsh.view.getTags():
            name = gmsh.option.getString(f"View[{tag}].Name")
            if name == U_values_name:
                view_tag = tag
                break

        if view_tag is None:
            raise ValueError(f"View with name '{U_values_name}' not found in the .pos file.")

        n_steps = int(gmsh.option.getNumber(f"View[{view_tag}].NbTimeStep"))

        times = []
        values = []
        for step in range(n_steps):
            data_type, tags, data, time, num_components = gmsh.view.getModelData(
                view_tag, step=step
            )
            if data_type.lower() != "nodedata":
                raise ValueError(f"Expected nodal data, but got {data_type} in step {step}.")
            
            if num_components != 3:
                raise ValueError(f"Expected {self.dim} components, but got {num_components} in step {step}.")

            times.append(time)
            values.append(data)

        self.T = np.array(times)
        self.U = np.array(values)[:,:, :self.dim]
        self.messages = None

        print(f"--- Successfully loaded {n_steps} steps for {self.U.shape[1]} nodes from Gmsh file ---")

    def solve(self):
        raise NotImplementedError("The solve method must be implemented in the subclass.")
