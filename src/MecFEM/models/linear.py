import matplotlib.pyplot as plt
import numpy as np
import copy
import datetime

from .base import Base

from ..mesh import Mesh
from ..elements import LinearFiniteElement
from ..utils import classification as cl

class Linear(Base):
    """
    Data structure for linear FE model
    
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
        - elems: list of LinearFiniteElement objects representing the elements in the mesh
        - boundary_elems: list of LinearFiniteElement objects representing the boundary elements in the mesh
        - U: array of nodal displacements at each time step (shape: (n_time_steps, n_nodes, dim))
        - T: array of time steps corresponding to the nodal displacements (shape: (n_time_steps,))
    """
    def __init__(self, mesh: Mesh, material) -> None:
        super().__init__(mesh, material, LinearFiniteElement)
        self._solver = cl.SolverClassification.LINEAR
        self.check_compatibility()

    def stiffness_matrix(self) -> np.ndarray:
        """
        Compute the global stiffness matrix for the linear FE model.
        """
        K = np.zeros((self.n_nodes, self.dim, self.n_nodes, self.dim))

        for i, elem in enumerate(self.elems):
            self.assemble(i, elem.stiffness_matrix(), K)

        return K
    
    def solve(
            self,
            dt: float=0.1, 
            t_end: float=1.0,
            F_VERBOSE: int=10, 
        ) -> None:
        """
        Solve the linear FE model.
        """
        time =0.0
        n_step = 1
        Un = np.zeros((self.n_dofs))
        Un = self.apply_displacement(Un, time)

        messages = []
        time_verbose = [0.0]
        U_verbose = [Un]
        
        self.update_elements(Un)
        K = self.stiffness_matrix().reshape((self.n_dofs, self.n_dofs))

        time = dt
        print("===== Starting linear solver =====")
        start_time = datetime.datetime.now()
        while time <= t_end:
            # print(f"Time: {time:.4f} / {t_end:.4f}")
            Un = np.zeros((self.n_dofs))
            Un = self.apply_displacement(Un, time)
            F_fixed_dofs = K[np.ix_(self.free_dofs, self.fixed_dofs)] @ Un[self.fixed_dofs]
            F_external = (self.volumetric_forces(time) + self.external_forces(time)).reshape((self.n_dofs, ))
            # print(K.shape)
            # print(F_fixed_dofs.shape)
            # print(F_external.shape)

            Un[self.free_dofs] = np.linalg.solve(K[np.ix_(self.free_dofs, self.free_dofs)], F_external[self.free_dofs] - F_fixed_dofs)
            
            if (np.isnan(Un).any() or np.isinf(Un).any()):
                print(f"--------------- Simulation Stopped ---------------")
                print(f"NaN or Inf values found in solution at time {time:.2f}")
                break

            if (n_step % F_VERBOSE == 0 or time > t_end - dt):
                U_verbose.append(Un)
                time_verbose.append(time)

                Dt = datetime.datetime.now() - start_time
                print(f"Time: {str(Dt).split('.')[0]} < {str((t_end - time)*Dt/time).split('.')[0]} | Simulation time: {time:.4f} / {t_end:.4f}", end="\r", flush=True)
                
            time += dt
            n_step += 1
        
        run_time = datetime.datetime.now() - start_time
        print(f"SIMULATION COMPLETED - RUN TIME: {run_time}")

        self.U = np.array(U_verbose).reshape((len(time_verbose), self.n_nodes, self.dim))
        self.T = np.array(time_verbose)
        self.messages = messages

        return None
