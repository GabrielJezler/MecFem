import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.interpolate import griddata
import os

def load_data(path):
    file_params = os.path.join(path, 'params.npz')
    file_data = os.path.join(path, 'out.npz')
    if os.path.exists(file_params) and os.path.exists(file_data):
        params = np.load(file_params, allow_pickle=False)
        data = np.load(file_data, allow_pickle=False)
        return data, params
    else:
        print("No data found.")
        return None, None

def make_dir(path):
    try:
        os.mkdir(path)
        print(f"Directory '{path}' created successfully.")
        return True
    except FileExistsError:
        print(f"Directory '{path}' already exists. The files will not be overwritten.")
        return False
    except PermissionError:
        print(f"Permission denied: Unable to create '{path}'. The files will not be saved.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}. The files will not be saved.")
        return False

def save_data(ani, sol, params, f_verbose, message=None, save_config=None):
    if save_config is None:
        save = input("\nSave animation as gif (1), save data as npz (2), both (3): ").strip()
        if save == '1' or save == '2' or save == '3':
            dir_name = input(r"""
Enter folder name - you can use the following parameters (put them between '\{\}'):
dt: time step
nNodes: number of nodes
        
Ex: results_{dt}_{nNodes}_{method}_{lamb}_{order}_{nIntPts}_{periodics}
Name: """).format(dt=f'dt{params.dt:.2e}', nNodes=f'nNodes{params.nNodes}', method=f'method{params.method}', lamb=f'lambda{params.lamb}', order=f'order{params.order}', nIntPts=f'nIntPts{params.nIntPts}', periodics=f'periodics{0 if params.periodics == None else 1}').strip().lower().replace(' ', '_').replace('.', '_').replace(',', '_')
        else:
            print("No data saved")
            return False
    else:
        print(params.periodics)
        dir_name = save_config['dirname'].format(dt=f'dt{params.dt:.2e}', nNodes=f'nNodes{params.nNodes}', method=f'method{params.method}', lamb=f'lambda{params.lamb}', order=f'order{params.order}', nIntPts=f'nIntPts{params.nIntPts}', periodics=f'periodics{0 if params.periodics == None else 1}').strip().lower().replace(' ', '_').replace('.', '_').replace(',', '_')
        if save_config['save_gif'] and save_config['save_data']:
            save = '3'
        elif save_config['save_gif']:
            save = '1'
        elif save_config['save_data']:
            save = '2'
        else:
            print("No data saved")
            return False

    dir_name = os.path.join('results', dir_name)
    logi = make_dir(dir_name)
    if logi:
        if save == '1':
            ani.save(os.path.join(dir_name, f'1d_animation.gif'), writer='pillow', progress_callback=lambda i, n: print(f'Saving frame {i+1} of {n}', end="\r", flush=True))
            print(f"Animation saved in: {dir_name}")
        elif save == '2':
            np.savez(os.path.join(dir_name, 'out.npz'), time=sol.t, X=sol.xNodes, Y=sol.yNodes, Z=sol.zNodes, C=sol.C, E=sol.E, Fi=sol.Fi, Fb=sol.Fb, Qm=sol.Qm, message=message)
            np.savez(os.path.join(dir_name, 'params.npz'), dt=params.dt, T=params.T, nNodes=params.nNodes, method=params.method, lamb=params.lamb, f_verbose=f_verbose, order=params.order, nIntPts=params.nIntPts, periodics=params.periodics)
            print(f"Data saved in: {dir_name}")
        elif save == '3':
            np.savez(os.path.join(dir_name, 'out.npz'), time=sol.t, X=sol.xNodes, Y=sol.yNodes, Z=sol.zNodes, C=sol.C, E=sol.E, Fi=sol.Fi, Fb=sol.Fb, Qm=sol.Qm, message=message)
            np.savez(os.path.join(dir_name, 'params.npz'), dt=params.dt, T=params.T, nNodes=params.nNodes, method=params.method, lamb=params.lamb, f_verbose=f_verbose, order=params.order, nIntPts=params.nIntPts, periodics=params.periodics)
            ani.save(os.path.join(dir_name, f'1d_animation.gif'), writer='pillow', progress_callback=lambda i, n: print(f'Saving frame {i+1} of {n}', end="\r", flush=True))
            print(f"Data and animation saved in: {dir_name}")
        else:
            print("No data saved")

def plot1D(sol, params, f_verbose, t_scale=1.0, show=True):
    L = np.max(sol.xNodes)
    mosaic = [
        [0, 0, 0, 1, 1, 1],
        [3, 3, 3, 4, 4, 4],
        [5, 5, 5, 5, 5, 5]
    ]
    fig, ax = plt.subplot_mosaic(mosaic, figsize=(15,8))

    order = np.argsort(sol.xNodes.flatten())
    
    ax[0].plot(sol.t, sol.E, label='Total')
    ax[0].plot(sol.t, sol.Fi, label='Interfacial')
    ax[0].plot(sol.t, sol.Fb, label='Bulk')
    # ax[1].plot(sol.t, np.gradient(sol.E, sol.t), label='Total')
    # ax[1].plot(sol.t, np.gradient(sol.Fi, sol.t), label='Interfacial')
    # ax[1].plot(sol.t, np.gradient(sol.Fb, sol.t), label='Bulk')
    ax[1].plot(sol.t, sol.Qm - sol.Qm[0])
    ax[3].plot(sol.xNodes[order], sol.C[0][order], label='Initial')
    ax[4].plot(sol.xNodes[order], sol.C[-1][order], label='Final')
    
    line_e = ax[0].axvline(sol.t[0], color='r')
    line_de = ax[1].axvline(sol.t[0], color='r')
    line_qm, = ax[1].plot(sol.t[0], 0, 'ro')
    line_c, = ax[5].plot(np.sort(sol.xNodes.flatten()), sol.C[0][order])

    def update(frame):
        line_c.set_data(sol.xNodes[order], sol.C[frame][order])

        line_e.set_xdata([sol.t[frame]]) 
        line_de.set_xdata([sol.t[frame]]) 

        line_qm.set_data([sol.t[frame]], [sol.Qm[frame] - sol.Qm[0]])

        fig.suptitle(f'Concentration field at t={sol.t[frame]:.2f}', weight='bold')
        return line_c, line_e, line_de, line_qm

    # Create the animation
    ani = FuncAnimation(fig, update, frames=range(0, len(sol.t)), interval=1000*f_verbose*params.dt/t_scale, repeat=True)
    ax[0].set_xlabel('t')
    ax[0].set_ylabel('E')
    ax[0].set_title('Energy')
    ax[0].legend(ncol=3)
    # ax[1].set_xlabel('t')
    # ax[1].set_ylabel(r'$\partial t E$')
    # ax[1].set_title('Energy rate')
    # ax[1].legend(ncol=3)
    ax[1].set_xlabel('t')
    ax[1].set_ylabel(r"$Q_m - Q_{m}(t=0)$")
    ax[1].set_title('Concentration integral')
    ax[3].set_xlabel('x')
    ax[3].set_ylabel('c')
    ax[3].set_xlim(0, L)
    ax[3].set_title('Initial')
    ax[4].set_xlabel('x')
    ax[4].set_ylabel('c')
    ax[4].set_xlim(0, L)
    ax[4].set_title('Final')
    ax[5].set_xlabel('x')
    ax[5].set_ylabel('c')
    ax[5].set_xlim(0, L)
    ax[5].set_title('Temporal evolution')

    fig.suptitle('Concentration field at t=0.0', weight='bold')
    fig.tight_layout()

    if show:
        plt.show()

    return ani

def plot2D(sol, params, f_verbose, t_scale=1.0, show=True):  
    Lx = np.max(sol.xNodes)
    nNodesX = sol.xNodes.shape[0]
    Ly = np.max(sol.yNodes)
    nNodesY = sol.xNodes.shape[0]

    mosaic = [
        [0, 1],
        [2, 3],
        [4, 4]
    ]

    fig, ax = plt.subplot_mosaic(mosaic, figsize=(8,8))
    colormap = 'winter'

    # Create a grid for the contour plot
    grid_x, grid_y = np.meshgrid(np.linspace(0,Lx,nNodesX), np.linspace(0,Ly,nNodesY))

    ax[0].plot(sol.t, sol.E)
    line_e, = ax[0].plot(sol.t[0], sol.E[0], 'ro')

    ax[1].plot(sol.t, sol.Qm - sol.Qm[0])
    line_qm, = ax[1].plot(sol.t[0], sol.Qm[0] - sol.Qm[0], 'ro')

    # Interpolate data onto the grid
    grid_C0 = griddata((sol.xNodes, sol.yNodes), sol.C[0], (grid_x, grid_y), method='linear')
    contour = ax[2].contourf(grid_x, grid_y, grid_C0[:,:,0], cmap=colormap, levels=20)
    colb = fig.colorbar(contour, ax=ax[2])

    grid_Cn = griddata((sol.xNodes, sol.yNodes), sol.C[-1], (grid_x, grid_y), method='linear')
    contour = ax[3].contourf(grid_x, grid_y, grid_Cn[:,:,0], cmap=colormap, levels=20)
    colb = fig.colorbar(contour, ax=ax[3])

    contour = ax[4].contourf(grid_x, grid_y, grid_C0[:,:,0], cmap=colormap, levels=20)
    colb = fig.colorbar(contour, ax=ax[4])

    def update(frame, contour=contour):
        # for c in contour.collections:
        #     c.remove()
        
        grid_C = griddata((sol.xNodes, sol.yNodes), sol.C[frame], (grid_x, grid_y), method='linear')

        contour = ax[4].contourf(grid_x, grid_y, grid_C[:,:,0], cmap=colormap, levels=20)
        colb.update_normal(contour)
        colb.update_ticks()

        line_e.set_data([sol.t[frame]], [sol.E[frame]])
        line_qm.set_data([sol.t[frame]], [sol.Qm[frame] - sol.Qm[0]])

        fig.suptitle(f'Concentration field at t={sol.t[frame]:.2f}', weight='bold')
        return contour, line_e, line_qm

    # Create the animation
    ani = FuncAnimation(fig, update, frames=range(0, len(sol.t)), interval=1000*f_verbose*params.dt/t_scale, repeat=True)
    ax[0].set_xlabel('t')
    ax[0].set_ylabel(4)
    ax[0].set_title('Interfacial energy')
    ax[1].set_xlabel('t')
    ax[1].set_ylabel(r"$Q_m - Q_{m}(t=0)$")
    ax[1].set_title('Concentration integral')
    ax[2].set_xlabel('x')
    ax[2].set_ylabel('y')
    ax[2].set_ylim(0, Ly)
    ax[2].set_xlim(0, Lx)
    ax[2].set_title('Initial')
    ax[3].set_xlabel('x')
    ax[3].set_ylabel('y')
    ax[3].set_ylim(0, Ly)
    ax[3].set_xlim(0, Lx)
    ax[3].set_title('Final')
    ax[4].set_xlabel('x')
    ax[4].set_ylabel('y')
    ax[4].set_ylim(0, Ly)
    ax[4].set_xlim(0, Lx)
    ax[4].set_title('Temporal evolution')

    fig.suptitle('Concentration field at t=0.0', weight='bold')
    fig.tight_layout()

    if show:
        plt.show()
    