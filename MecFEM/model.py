from email.mime import message
import numpy as np
import copy
import datetime

from .mesh import Mesh
from .element import NonLinearFiniteElement
from .boundary_conditions import BCStep

class NonLinearFEModel:
    """
    Data structure for FE model
    
    Attributes:
        - dim: mesh dimension
        - nNodes: number of nodes
        - connect: table of connectivity (list of lists)

            Example: 
            
                connect=[
                    [node1_elem1, node2_elem1, ..., nodeN_elem1],

                    [node1_elem2, node2_elem2, ..., nodeN_elem2],
                    
                    ...
                    
                    [node1_elemM, node2_elemM, ..., nodeN_elemM]
                ]

        - material: Material object defining the constitutive behavior
    """
    def __init__(self, mesh: Mesh, material) -> None:
        self.dim: int = mesh.dim
        self.n_nodes: int = mesh.n_nodes
        self.connect: np.array = mesh.get_connectivity_matrix()

        self.free_dofs = np.arange(self.n_nodes * self.dim)
        self.fixed_dofs = np.array([])

        self.elems: list[NonLinearFiniteElement] = []
        self.boundary_elems: list[NonLinearFiniteElement] = []

        self.material = material

        for elem in mesh.elems[self.dim]:
            x_nodes = mesh.get_nodes_coodinates_by_element(elem.id, self.dim)
            self.elems.append(NonLinearFiniteElement(elem, x_nodes))
        
        self._volumetric_force_steps: list[BCStep] = []
        self._external_forces: list[BCStep] = []
    
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
    
    def add_volumetric_force(self, step: BCStep) -> None:
        """
        Add volumetric force to the model.

        Parameters
        ----------
        f_nodes : np.ndarray
            Function that takes nodal coordinates and returns nodal forces.

        Returns
        -------
        None.

        """
        if isinstance(step, BCStep):
            self._volumetric_force_steps.append(step)
        else:
            raise TypeError("step must be an instance of BCStep")
        
        return None
    
    def add_external_force(self, f_nodes: np.ndarray) -> None:
        """
        Add external force to the model.

        Parameters
        ----------
        f_nodes : np.ndarray
            Function that takes nodal coordinates and returns nodal forces.

        Returns
        -------
        None.

        """
        if not f_nodes.shape == (self.n_nodes, self.dim):
            raise ValueError("External force shape mismatch")
        
        self._external_forces.append(f_nodes)
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
        V[*([iNod, slice(None)] * (V.ndim // 2))] += vNod
        return None
    
    def update_elements(self, U: np.ndarray) -> None:
        """
        Update all elements based on nodal displacements and material properties.

        Parameters
        ----------
        U : ndarray
            Nodal displacement field. This is an array of shape (n_nodes, dim).
        material : Material
            Material object defining the constitutive behavior.

        Returns
        -------
        None.

        """
        for e in range(self.n_elements):
            u_node = self.extract(U, e)
            self.elems[e].update(u_node, self.material)
        
        return None
    
    def internal_forces(self, U) -> np.ndarray:
        """
        Compute global internal force vector.

        Returns
        -------
        Fint : ndarray
            Global internal force vector. This is an array of shape (n_nodes, dim).

        """
        Fint = np.zeros((self.n_nodes, self.dim))

        for i, elem in enumerate(self.elems):
            self.assemble(i, elem.internal_force(), Fint)
        
        return Fint
    
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
            # volumetric_forces_elem = np.sum(np.array([step.interp(t)(elem.x_nodes[:, 0:elem.dim], elem.fshape) for step in self._volumetric_force_steps]), axis=0)

            volumetric_forces_elem = np.sum([step.interp(t)(elem.x_nodes[:, 0:elem.dim], elem.fshape()) for step in self._volumetric_force_steps], axis=0)

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

        if self._external_forces == []:
            return Fext

        for i, elem in enumerate(self.elems):
            external_forces_elem = np.sum(np.array([f(elem.x_nodes[:, 0:elem.dim], elem.fshape) for f in self._external_forces]), axis=0)

            self.assemble(i, elem.external_force(external_forces_elem), Fext)

        return Fext
    
    def residual(self, U: np.ndarray, t: float=0.0) -> np.ndarray:
        """
        Compute global residual vector.

        Parameters
        ----------
        U : ndarray
            Nodal displacement field. This is an array of shape (n_nodes, dim).

        t : float
            Current time.

        Returns
        -------
        R : ndarray
            Global residual vector. This is an array of shape (n_nodes, dim).

        """
        self.update_elements(U)

        R = self.internal_forces(U) - (self.volumetric_forces(t) + self.external_forces(t))
        return R
    
    def solve(
            self,
            U0: np.ndarray,
            dt: float=0.1, 
            t_end: float=1.0,
            F_VERBOSE: int=10, 
            PRECISION: float=1e-15, 
            TOLERANCE: float=1e-6, 
            MAX_ITER: int=10,
            FULL_VERBOSE: bool=False, 
        ):
        """
        Solve the nonlinear FE model using the Newton-Raphson method.

        Returns
        -------
        U : ndarray
            Nodal displacement field. This is an array of shape (n_nodes, dim).

        """
        time = 0.0

        time_verbose = [0.0]
        U_verbose = [U0]

        messages = []

        self.update_elements(U0, self.material)

        n_step = 1
        Un_1 = U0.reshape((self.n_nodes, self.dim))

        time = dt

        print("===== Starting nonlinear solver =====")
        start_time = datetime.datetime.now()
        while time < t_end:
            Un = Un_1
            
            R = self.residual(Un, time)
            norm_R0 = np.linalg.norm(R[np.ix_(self.free_dofs)])
            norm_R = 1.0

            iter = 1
            if FULL_VERBOSE:
                print(f'------------------------ Time = {time:.6f} ------------------------')
                print(f'Newton-Raphson iteration {iter:>2} | ||r||: {norm_R:.3e}')
            
            while norm_R > TOLERANCE and norm_R > PRECISION:
                # Compute tangent stiffness matrix
                tangent = None ### To do

                dU = np.linalg.solve(tangent[np.ix_(self.free_dofs,self.free_dofs)], -R[np.ix_(self.free_dofs)])

                norm_dU = np.linalg.norm(dU)
                if (norm_dU < PRECISION):
                    if not stagnation:
                        print(f"\nERROR - CONVERGENCE: dU stagnation started at t = {time:.4f}\n")
                        messages.append(f"ERROR - CONVERGENCE: dU stagnation started at t = {time:.4f}")
                        stagnation = True
                    break

                Un[np.ix_(self.free_dofs)] = Un[np.ix_(self.free_dofs)] + dU

                R = self.residual(Un, time + dt)
                norm_R = np.linalg.norm(R[np.ix_(self.free_dofs)]) / norm_R0

                iter += 1
                if FULL_VERBOSE:
                    print(f'Newton-Raphson iteration {iter:>2} | ||r||: {norm_R:.4e} | ||dU||: {np.linalg.norm(dU):.3e}')

                if iter >= MAX_ITER:
                    print(f"\nERROR - CONVERGENCE: max iteration reached at t = {time:.4f} | ||r||: {norm_R:.3e} | iteration = {iter}") 
                    messages.append(f"ERROR - CONVERGENCE: max iteration reached at t = {time:.4f} | ||r||: {norm_R:.3e}")
                    break

            if FULL_VERBOSE:
                if norm_R <= TOLERANCE:
                    print(f"SUCCESFULL ITERATION AT TIME t = {time:.4e}: norm = {norm_R:.3e}")
            
            if (np.isnan(Un).any() or np.isinf(Un).any()):
                print(f"--------------- Simulation Stopped ---------------")
                print(f"NaN or Inf values found in solution at time {time:.2f}")
                break

            if (n_step % F_VERBOSE == 0 or time > t_end - dt):
                U_verbose.append(Un)
                time_verbose.append(time)

                Dt = datetime.now() - start_time
                print(f"Time: {str(Dt).split('.')[0]} < {str((t_end - time)*Dt/time).split('.')[0]} | Simulation time: {time:.4f} / {t_end:.4f} | ||r||: {norm_R:.3e} at iteration {iter:<2}", end="\r", flush=True)
        
            Un_1 = Un
            time += dt
            n_step += 1
        
        run_time = datetime.now() - start_time
        print(f"SIMULATION COMPLETED - RUN TIME: {run_time}")

    def sigma(self, U: np.ndarray, averaged=True) -> np.ndarray:
        """
        Get Cauchy stress at integration points for element elem_id.

        Parameters
        ----------
        U : np.ndarray
            Nodal displacement field. This is an array of shape (n_nodes, dim).
        averaged : bool, optional
            If True, return averaged stress at nodes. If False, return stress at integration points. The default is True.

        Returns
        -------
        sigma : ndarray
            Cauchy stress at nodes. This is an array of shape (n_nodes, dim, dim).

        """
        sigma = np.zeros((self.n_nodes, self.dim, self.dim))

        n_elem = np.zeros((self.n_nodes))
        for e, elem in enumerate(self.elems):
            u_nodes = self.extract(U, e)
            sigma_elem = elem.sigma(u_nodes, self.material)

            sigma[self.connect[e], :, :] += sigma_elem
            n_elem[self.connect[e]] += 1

        return self.get_nodes_coordinates(), sigma / n_elem[:, None, None]

