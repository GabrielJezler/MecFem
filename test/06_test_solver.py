import MecFEM as mf
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "figure.figsize": (10, 8),
    "figure.titlesize": 24,
    "axes.titlesize": 20,
    "font.family": "Courier New",
    "font.size": 16,
    "savefig.format": "pdf",
})

def f_volumetric(x:np.ndarray) -> np.ndarray:
    """
    Example volumetric force function.

    Parameters
    ----------
    x : ndarray
        Coordinates where the force is evaluated. This is an array of shape (n_nodes, dim).

    Returns
    -------
    f : ndarray
        Volumetric force vector at the given coordinates. This is an array of shape (n_nodes, dim).

    """
    f = np.zeros_like(x)
    f[:, 1] = -9.81  # Gravity in negative y-direction
    return f

def fixed_disp(X:np.ndarray) -> np.ndarray:
    """
    Example fixed displacement function.

    Parameters
    ----------
    x : ndarray
        Coordinates where the displacement is evaluated. This is an array of shape (n_dofs,).

    Returns
    -------
    u : ndarray | float
        Displacement vector at the given coordinates. This is an array of shape (n_dofs,).

    """
    return np.zeros(X.shape[0])

def x_disp(X:np.ndarray) -> np.ndarray:
    """
    Example displacement function.

    Parameters
    ----------
    X : ndarray
        Coordinates where the displacement is evaluated. This is an array of shape (n_dofs,).

    Returns
    -------
    u : ndarray | float
        Displacement vector at the given coordinates. This is an array of shape (n_dofs,).

    """

    return 0.001 * np.ones(X.shape[0])

def f_volumetric(x:np.ndarray, g) -> np.ndarray:
    """
    Example volumetric force function.

    Parameters
    ----------
    x : ndarray
        Coordinates where the force is evaluated. This is an array of shape (n_nodes, dim).
    g : float
        Gravity magnitude.

    Returns
    -------
    f : ndarray
        Volumetric force vector at the given coordinates. This is an array of shape (n_nodes, dim).

    """
    f = np.zeros_like(x)
    f[:, 1] = g
    return f


def test():
    mf.mesh.generate.generate_rectangle_mesh(
        1.0, 0.5, 16, 8, "mesh/rect.msh"
    )
    
    mesh = mf.mesh.Mesh("mesh/rect.msh", dim=2)

    mesh.plot(nodes_ids=False, elems_ids=False, zoom_out=0.25)

    plt.show()

    material = mf.materials.non_linear.StVenantKirchhoffElasticity(E=200.0e9, nu=0.3)

    model = mf.models.NonLinear(
        mesh,
        material
    )

    x_nodes = mesh.get_nodes_coordinates()

    left_nodes = np.where(x_nodes[:, 0] == 0.0)[0]
    right_nodes = np.where(x_nodes[:, 0] == 1.0)[0]

    fix_disp_step = mf.boundary_conditions.Displacement(fixed_disp)
    x_disp_step = mf.boundary_conditions.Displacement(x_disp)

    # Fix X and Y displacements at the left edge
    model.add_displacement_bc(
        np.concatenate((left_nodes * 2, left_nodes * 2 + 1)),
        mf.boundary_conditions.BCStep(
            times=[0.0, 1.0],
            values=[0.0 * fix_disp_step, 1.0 * fix_disp_step]
        )
    )

    # Fix Y displacements at the right edge
    model.add_displacement_bc(
        right_nodes * 2 + 1,
        mf.boundary_conditions.BCStep(
            times=[0.0, 1.0],
            values=[0.0 * fix_disp_step, 1.0 * fix_disp_step]
        )
    )

    # Impose X displacements at the right edge
    model.add_displacement_bc(
        right_nodes * 2,
        mf.boundary_conditions.BCStep(
            times=[0.0, 1.0],
            values=[0.0 * x_disp_step, 1.0 * x_disp_step]
        )
    )

    x_elements_cg = mesh.get_elements_cg_coordinates()

    lower_elements = np.where(x_elements_cg[:, 1] < 0.25)[0]
    upper_elements = np.where(x_elements_cg[:, 1] >= 0.25)[0]

    lower_elements_id = [mesh.elems[mesh.dim][i].id for i in lower_elements]
    upper_elements_id = [mesh.elems[mesh.dim][i].id for i in upper_elements]

    f = mf.boundary_conditions.VolumetricForce(lambda X: f_volumetric(X, g=-9.81 * 1e7))

    model.add_volumetric_force(
        step=mf.boundary_conditions.BCStep(
            times=[0.0, 1.0],
            values=[f * 0.0, f * 1.0]
        ),
        elems_id=None # Apply to all elements
    )

    fig, ax = plt.subplots()

    mesh.plot(ax=ax, nodes_ids=False, elems_ids=False, zoom_out=0.25)

    model.plot_bc(ax=ax, time=1.0)

    ax.legend(loc='center right', ncol=1, bbox_to_anchor=(1.0, 0.5))
    plt.show()

    model.solve(
        dt=0.1,
        t_end=1.0,
        F_VERBOSE=1,
        MAX_ITER=50
    )

    fig, ax = plt.subplots()

    mesh.plot(
        ax,
        nodes_marker=False,
        nodes_ids=False,
        elems_ids=False,
        zoom_out=0.25
    )

    ax = mf.post.vector.plot_2d_field(
        model, 
        model.U[-1], 
        component="y", 
        ax=ax, 
        label='Displacement field'
    )

    plt.show()

    fig, ax = plt.subplots()

    sigma = model.sigma(averaged=True)

    mesh.plot(
        ax=ax,
        nodes_marker=False,
        nodes_ids=False,
        elems_ids=False,
        zoom_out=0.25
    )
    

    mf.post.tensor.plot_2d_field(
        model, 
        sigma[-1, :, :], 
        ax=ax, 
        component="vm", 
        label='VM Stress'
    )

    plt.show()

    fig, ax = plt.subplots()

    mesh.plot(
        ax,
        nodes_marker=False,
        nodes_ids=False,
        elems_ids=False,
        zoom_out=0.25
    )

    ax, ani = mf.post.vector.animate_2d_displacement(model, scale=100, ax=ax, label='Displacement magnitude', zoom_out=0.25, interval=200)

    fig.suptitle("Displacement animation")
    plt.show()

    mesh.write_element_tensor2_data(
        values=sigma, 
        times=model.T,
        label="Stress"
    )

    mesh.write_nodal_vector_data(
        values=model.U, 
        times=model.T,
        label="Displacement"
    )
    

if __name__ == "__main__":
    test()
