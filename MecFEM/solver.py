from datetime import datetime
import numpy as np
from .data_struct import Solution

def solve_linear(mesh, model, params, f_verbose=10):
    time = params.dt
    t_verbose = [0.0]

    message = []

    model.updateModel(params.C0)
    C = params.C0
    C_verbose = [params.C0]
    energy = model.computeGlobalEnergies(params.C0)
    E_verbose = [energy[0]]
    Fi_verbose = [energy[1]]
    Fb_verbose = [energy[2]] 
    Qm_verbose = [model.computeGlobalQuantityofMaterial(params.C0)]

    if params.periodics is not None:
        P_ = model.computeP(params.periodics)
        P = np.block([[P_, np.zeros_like(P_)], [np.zeros_like(P_), P_]])

    start_time = datetime.now()
    tStep = 1
    print("Starting simulation...")
    while time < params.T - params.dt/2:
        model.updateModel(C)

        K = model.computeGlobalStiffness(params.dt)
        F = model.computeGlobalForce(C, params.dt)

        if params.periodics is None:
            X = np.linalg.solve(K,F)
        else:
            K_ = P.T @ K @ P
            F_ = P.T @ F
            X_ = np.linalg.solve(K_, F_)
            X = P @ X_

        if np.isnan(X).any() or np.isinf(X).any():
            print(f"--------------- Simulation Stopped ---------------")
            print(f"NaN or Inf values found in solution at time {time:.3f}")
            break

        C = X[:model.nNodes]
        W = X[model.nNodes:]

        if (tStep % f_verbose == 0 or time >= params.T-params.dt):
            energy = model.computeGlobalEnergies(C)
            t_verbose.append(time)
            C_verbose.append(C)
            E_verbose.append(energy[0])
            Fi_verbose.append(energy[1])
            Fb_verbose.append(energy[2])
            Qm_verbose.append(model.computeGlobalQuantityofMaterial(C))
            Dt = datetime.now() - start_time
            print(f"Time: {str(Dt).split('.')[0]} < {str((params.T-time)*Dt/time).split('.')[0]} | Simulation time: {time:.6f} / {params.T:.6f}", end="\r", flush=True)
        
        tStep += 1
        time += params.dt

    run_time = datetime.now() - start_time
    print(f"\n\nSIMULATION COMPLETED - RUN TIME: {run_time}")

    sol = Solution(mesh.nodesCoords, t_verbose, C_verbose, E_verbose, Fi_verbose, Fb_verbose, Qm_verbose)
    message.append(f'RUNTIME:{run_time}')
    return sol, message

def solve_nonlinear(mesh, model, params, f_verbose=10, FULL_VERBOSE=False, PRECISION=1e-15, TOLERANCE=1e-6, MAX_ITER=10):
    time = params.dt
    t_verbose = [0.0]
    message = []

    model.updateModel(params.C0)
    Cn_1 = params.C0
    Wn_1 = model.computeInternalEnergy(params.C0)
    C_verbose = [params.C0]
    energy = model.computeGlobalEnergies(params.C0)
    E_verbose = [energy[0]]
    Fi_verbose = [energy[1]]
    Fb_verbose = [energy[2]]
    Qm_verbose = [model.computeGlobalQuantityofMaterial(params.C0)]

    start_time = datetime.now()
    tStep = 1
    print("Starting simulation...")
    stagnation = False
    while time < params.T:
        Cn = Cn_1
        Wn = Wn_1
        model.updateModel(Cn)
        r = model.computeGlobalResidual(Cn, Wn, Cn_1, params.dt)
        norm_r0 = np.linalg.norm(r)
        norm_r = 1.0

        iteration = 1
        if FULL_VERBOSE:
            print(f'------------------------ Time = {time:.6f} ------------------------')
            print(f'Newton-Raphson iteration {iteration:>2} | ||r||: {norm_r:.3e}')
        while norm_r > TOLERANCE and norm_r > PRECISION:
            tangent = model.computeGlobalTangent(Wn, params.dt)

            dX = np.linalg.solve(tangent, -r)

            norm_dX = np.linalg.norm(dX)
            if (norm_dX < PRECISION):
                if not stagnation:
                    print(f"\nERROR - CONVERGENCE: dX stagnation started at t = {time:.4f}\n")
                    message.append(f"ERROR - CONVERGENCE: dX stagnation started at t = {time:.4f}")
                    stagnation = True
                break

            dC = dX[:model.nNodes]
            dW = dX[model.nNodes:]

            Cn = Cn + dC
            Wn = Wn + dW

            model.updateModel(Cn)

            r = model.computeGlobalResidual(Cn, Wn, Cn_1, params.dt)
            norm_r = np.linalg.norm(r)/norm_r0
            iteration += 1
            if FULL_VERBOSE:
                print(f'Newton-Raphson iteration {iteration:>2} | ||r||: {norm_r:.4e} | ||dC||: {np.linalg.norm(dC):.3e} | ||dW||: {np.linalg.norm(dW):.3e}')

            if iteration >= MAX_ITER:
                print(f"\nERROR - CONVERGENCE: max iteration reached at t = {time:.4f} | ||r||: {norm_r:.3e} | iteration = {iteration}") 
                message.append(f"ERROR - CONVERGENCE: max iteration reached at t = {time:.4f} | ||r||: {norm_r:.3e}")
                break

        if FULL_VERBOSE:
            if norm_r <= TOLERANCE:
                print(f"SUCCESFULL ITERATION AT TIME t = {time:.4e}: norm = {norm_r:.3e}")

        if (np.isnan(Cn).any() or np.isinf(Cn).any() or np.isnan(Wn).any() or np.isinf(Wn).any()):
            print(f"--------------- Simulation Stopped ---------------")
            print(f"NaN or Inf values found in solution at time {time:.2f}")
            break

        if (tStep % f_verbose == 0 or time > params.T-params.dt):
            C_verbose.append(Cn)
            energy = model.computeGlobalEnergies(Cn)
            E_verbose.append(energy[0])
            Fi_verbose.append(energy[1])
            Fb_verbose.append(energy[2])
            t_verbose.append(time)
            Qm_verbose.append(model.computeGlobalQuantityofMaterial(Cn))
            Dt = datetime.now() - start_time
            print(f"Time: {str(Dt).split('.')[0]} < {str((params.T-time)*Dt/time).split('.')[0]} | Simulation time: {time:.4f} / {params.T:.4f} | ||r||: {norm_r:.3e} at iteration {iteration:<2}", end="\r", flush=True)
        
        Cn_1 = Cn
        Wn_1 = Wn
        tStep += 1
        time += params.dt

    run_time = datetime.now() - start_time
    print(f"SIMULATION COMPLETED - RUN TIME: {run_time}")

    sol = Solution(mesh.nodesCoords, t_verbose, C_verbose, E_verbose, Fi_verbose, Fb_verbose, Qm_verbose)
    message.append(f'RUNTIME:{run_time}')
    return sol, message
