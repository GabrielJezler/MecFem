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

    return 0.1 * np.ones(X.shape[0])

if __name__ == "__main__":
    mf.mesh.generate.generate_rectangle_mesh(
        1.0, 0.5, 32, 16, "mesh/rect.msh"
    )
    mesh = mf.mesh.read.read_gmsh_mesh("mesh/rect.msh", dim=2)

    mf.mesh.plot_mesh(mesh, nodes_ids=False, elems_ids=False, zoom_out=0.25)

    plt.show()

    material = mf.materials.non_linear.StVenantKirchhoffElasticity(E=200.0e9, nu=0.3)

    model = mf.model.NonLinearFE(
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

    model.solve(
        dt=0.1,
        t_end=1.0,
        F_VERBOSE=1,
        MAX_ITER=50
    )

    
    fig, ax = plt.subplots()
    mf.mesh.plot_mesh(mesh, ax, nodes_ids=False, elems_ids=False, zoom_out=0.25)

    ax = mf.post.vector.plot_2d_field(model, model.U[-1], component="mag", ax=ax, label='Displacement field')
    
    plt.show()

    fig, ax = plt.subplots()

    sigma = model.sigma(averaged=True)
    mf.mesh.plot_mesh(mesh, ax, nodes_ids=False, elems_ids=False, zoom_out=0.25)
    
    mf.post.tensor.plot_2d_field(model, sigma[-1, :, :], ax=ax, component="vm", label='VM Stress')
    
    plt.show()

    mf.mesh.write.element_tensor2_data("mesh/rect.msh", "out_test.msh", mesh, sigma, times=model.T, label="Stress")

    mf.mesh.write.node_vector_data("out_test.msh", "out_test.msh", mesh, model.U, model.T, label="Displacement")