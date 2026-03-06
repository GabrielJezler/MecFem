import matplotlib.pyplot as plt
import numpy as np

import MecFEM as mf

plt.rcParams.update({
    "figure.figsize": (10, 8),
    "figure.titlesize": 24,
    "figure.autolayout":True,
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

def rx_disp(X:np.ndarray, dr:float) -> np.ndarray:
    """
    Example radial displacement function along x axis.

    Parameters
    ----------
    X : ndarray
        Coordinates where the displacement is evaluated. This is an array of shape (n_dofs,).
    dr : float
        Radial displacement magnitude at the arc.

    Returns
    -------
    u : ndarray | float
        Displacement vector at the given coordinates. This is an array of shape (n_dofs,).

    """

    return dr * X[:, 0] / np.linalg.norm(X, axis=1)

def ry_disp(X:np.ndarray, dr:float) -> np.ndarray:
    """
    Example radial displacement function along y axis.

    Parameters
    ----------
    X : ndarray
        Coordinates where the displacement is evaluated. This is an array of shape (n_dofs,).
    dr : float
        Radial displacement magnitude at the arc.
    
    Returns
    -------
    u : ndarray | float
        Displacement vector at the given coordinates. This is an array of shape (n_dofs,).

    """

    return dr * X[:, 1] / np.linalg.norm(X, axis=1)


if __name__ == "__main__":
    mesh = mf.mesh.Mesh("../mesh/cylinder_quad.msh",dim=2)

    fig, ax = plt.subplots()

    mesh.plot(ax=ax, nodes_ids=False, elems_ids=False, zoom_out=0.25)

    selector = mf.chart_selectors.node.LassoSelector(ax)

    plt.show()

    material = mf.materials.linear.IsotropicElasticity(E=10.0e6, nu=0.45)

    model = mf.models.Linear(
        mesh,
        material
    )

    x_nodes = mesh.get_nodes_coordinates()

    left_nodes = np.arange(model.n_nodes)[np.isclose(x_nodes[:, 0], 0.0)]

    down_nodes = np.arange(model.n_nodes)[np.isclose(x_nodes[:, 1], 0.0)]
    
    arc_in = np.arange(model.n_nodes)[np.isclose(x_nodes[:, 0]**2 + x_nodes[:, 1]**2, 0.02**2)]
    
    arc_out = np.arange(model.n_nodes)[np.isclose(x_nodes[:, 0]**2 + x_nodes[:, 1]**2, 0.06**2)]
    arc_out = np.setdiff1d(arc_out, np.concatenate((left_nodes, down_nodes)))

    left_nodes = np.setdiff1d(left_nodes, arc_in)
    down_nodes = np.setdiff1d(down_nodes, arc_in)


    fix_disp_step = mf.boundary_conditions.Displacement(fixed_disp)
    rx_disp_step = mf.boundary_conditions.Displacement(lambda X: rx_disp(X, dr=1e-5))
    ry_disp_step = mf.boundary_conditions.Displacement(lambda X: ry_disp(X, dr=1e-5))

    # Fix X displacements at the left edge
    model.add_displacement_bc(
        2 * left_nodes,
        mf.boundary_conditions.BCStep(
            times=[0.0, 1.0],
            values=[0.0 * fix_disp_step, 1.0 * fix_disp_step]
        )
    )

    # Fix Y displacements at the right edge
    model.add_displacement_bc(
        2 * down_nodes + 1,
        mf.boundary_conditions.BCStep(
            times=[0.0, 1.0],
            values=[0.0 * fix_disp_step, 1.0 * fix_disp_step]
        )
    )

    # Impose radial displacements at the arc out edge
    # At x dofs
    model.add_displacement_bc(
        2 * arc_in,
        mf.boundary_conditions.BCStep(
            times=[0.0, 1.0],
            values=[0.0 * rx_disp_step, 1.0 * rx_disp_step]
        )
    )

    # At y dofs
    model.add_displacement_bc(
        2 * arc_in + 1,
        mf.boundary_conditions.BCStep(
            times=[0.0, 1.0],
            values=[0.0 * ry_disp_step, 1.0 * ry_disp_step]
        )
    )

    fig, ax = plt.subplots()

    mesh.plot(ax=ax, nodes_ids=False, elems_ids=False, zoom_out=0.25)

    model.plot_bc(ax=ax)

    ax.legend(loc='center left', ncol=1, bbox_to_anchor=(1.0, 0.5))
    plt.show()

    model.solve(
        dt=0.1,
        t_end=1.0,
        F_VERBOSE=1,
    )

    fig, ax = plt.subplots(1,2)
    ax[0] = mesh.plot(ax=ax[0], nodes_marker=False, nodes_ids=False, elems_ids=False, zoom_out=0.1)
    ax[1] = mesh.plot(ax=ax[1], nodes_marker=False, nodes_ids=False, elems_ids=False, zoom_out=0.1)
    
    ax[0] = mf.post.vector.plot_2d_field(model, model.U[-1], ax=ax[0], component="Mag", label='Displacement')
    ax[1] = mf.post.vector.plot_2d_arrows(model, model.U[-1], ax=ax[1], scale=1/5000, label='Displacement vectors')

    fig.suptitle("Displacement")
    plt.show()

    sigma = model.sigma(averaged=True)

    fig, ax = plt.subplots()
    ax = mesh.plot(ax=ax, nodes_marker=False, nodes_ids=False, elems_ids=False, zoom_out=0.25)

    ax = mf.post.tensor.plot_2d_field(model, sigma[-1], ax=ax, component="VM", label='Von Mises Stress')

    fig.suptitle("Von Mises stress field")
    plt.show()

    fig, ax = plt.subplots()
    ax = mesh.plot(ax=ax, nodes_marker=False, nodes_ids=False, elems_ids=False, zoom_out=0.25)

    ax = mf.post.vector.plot_2d_arrows(model, model.reactions()[-1,:,:], ax=ax, scale=200, label='Reaction vectors')

    fig.suptitle("Reaction vectors")
    plt.show()

    fig, ax = plt.subplots()
    ax = mesh.plot(ax=ax, nodes_marker=False, nodes_ids=False, elems_ids=False, zoom_out=0.25)

    ax, ani = mf.post.vector.animate_2d_displacement(model, scale=1000, ax=ax, label='Displacement magnitude', zoom_out=0.25, interval=200)

    fig.suptitle("Displacement animation")
    plt.show()

    # mf.mesh.write.element_tensor2_data("mesh/cylinder_quad.msh", "out_test.msh", mesh, sigma, times=model.T, label="Stress")

    # mf.mesh.write.node_vector_data("out_test.msh", "out_test.msh", mesh, model.U, model.T, label="Displacement")