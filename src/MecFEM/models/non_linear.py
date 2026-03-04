import matplotlib.pyplot as plt
import numpy as np
import copy
import datetime

from .base import Base

from ..mesh import Mesh
from ..elements import NonLinearFiniteElement
from ..boundary_conditions import BCStep

class NonLinear(Base):
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
    def __init__(self, mesh: Mesh, material) -> None:
        super().__init__(mesh, material, NonLinearFiniteElement)

        self.R:np.ndarray | None = None # Residual
    
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
    
    def tangent_matrix(self, U: np.ndarray, t: float=0.0) -> np.ndarray:
        K = np.zeros((self.n_nodes, self.dim, self.n_nodes, self.dim))

        for i, elem in enumerate(self.elems):
            self.assemble(i, elem.internal_tangent_matrix(), K)

        return K

    def solve(
            self,
            dt: float=0.1, 
            t_end: float=1.0,
            F_VERBOSE: int=10, 
            PRECISION: float=1e-15, 
            TOLERANCE: float=1e-6, 
            MAX_ITER: int=10,
            FULL_VERBOSE: bool=False, 
        ) -> None:
        """
        Solve the nonlinear FE model using the Newton-Raphson method.

        Returns
        -------
        U : ndarray
            Nodal displacement field. This is an array of shape (n_nodes, dim).

        """
        time = 0.0        

        n_step = 1
        Un_1 = np.zeros((self.n_dofs))
        Un_1 = self.apply_displacement(Un_1, time)

        messages = []
        time_verbose = [0.0]
        U_verbose = [Un_1]
        R_verbose = [self.residual(Un_1.reshape((self.n_nodes, self.dim)), time)]

        self.update_elements(Un_1.reshape((self.n_nodes, self.dim)))

        time = dt
        print("===== Starting nonlinear solver =====")
        start_time = datetime.datetime.now()
        while time < t_end:
            Un = copy.deepcopy(Un_1)
            Un = self.apply_displacement(Un, time)
            
            R = self.residual(Un.reshape((self.n_nodes, self.dim)), time).reshape((self.n_dofs))
            norm_R0 = np.linalg.norm(R[np.ix_(self.free_dofs)])
            norm_R = 1.0

            stagnation = False
            iter = 1
            if FULL_VERBOSE:
                print(f'------------------------ Time = {time:.6f} ------------------------')
                print(f'Newton-Raphson iteration {iter:>2} | ||r||: {norm_R:.3e}')
            
            while norm_R > TOLERANCE and norm_R > PRECISION:
                tangent = self.tangent_matrix(Un.reshape((self.n_nodes, self.dim)), time).reshape((self.n_dofs, self.n_dofs))

                dU = np.linalg.solve(tangent[np.ix_(self.free_dofs,self.free_dofs)], -R[np.ix_(self.free_dofs)])

                norm_dU = np.linalg.norm(dU)
                if (norm_dU < PRECISION):
                    if not stagnation:
                        print(f"\nERROR - CONVERGENCE: dU stagnation started at t = {time:.4f}\n")
                        messages.append(f"ERROR - CONVERGENCE: dU stagnation started at t = {time:.4f}")
                        stagnation = True
                    break

                Un[np.ix_(self.free_dofs)] = Un[np.ix_(self.free_dofs)] + dU

                R = self.residual(Un.reshape((self.n_nodes, self.dim)), time + dt).reshape((self.n_dofs))
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
                R_verbose.append(R.reshape((self.n_nodes, self.dim)))

                Dt = datetime.datetime.now() - start_time
                print(f"Time: {str(Dt).split('.')[0]} < {str((t_end - time)*Dt/time).split('.')[0]} | Simulation time: {time:.4f} / {t_end:.4f} | ||r||: {norm_R:.3e} at iteration {iter:<2}", end="\r", flush=True)
        
            Un_1 = copy.deepcopy(Un)
            time += dt
            n_step += 1
        
        run_time = datetime.datetime.now() - start_time
        print(f"SIMULATION COMPLETED - RUN TIME: {run_time}")

        self.U = np.array(U_verbose).reshape((len(time_verbose), self.n_nodes, self.dim))
        self.T = np.array(time_verbose)
        self.R = np.array(R_verbose)
        self.messages = messages

        return None
