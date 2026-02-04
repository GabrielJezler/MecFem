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

def f_volumetric1(x:np.ndarray) -> np.ndarray:
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

def f_volumetric2(x:np.ndarray) -> np.ndarray:
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
    f[:, 0] = -9.81  # Gravity in negative x-direction
    return f

if __name__ == "__main__":
    mf.mesh.generate.generate_rectangle_mesh(
        1.0, 0.5, 8, 4, "mesh/rect.msh"
    )
    mesh = mf.mesh.read.read_gmsh_mesh("mesh/rect.msh", dim=2)

    material = mf.materials.IsotropicElasticity(E=200.0e9, nu=0.3)

    model = mf.NonLinearFEModel(
        mesh,
        material
    )

    x_nodes = mesh.get_nodes_coordinates()

    f1 = mf.boundary_conditions.VolumetricForce(f_volumetric1)
    f2 = mf.boundary_conditions.VolumetricForce(f_volumetric2)
    f = (f1 + f2) /2

    bc_step = mf.boundary_conditions.BCStep(
        times=[0.0, 1.0, 2.0],
        values=[f * 0.0, f * 1.0, f * 0.0]
    )

    model.add_volumetric_force(bc_step)
    model.add_volumetric_force(bc_step)

    U = np.zeros((mesh.n_nodes, mesh.dim))
    U[:, 0] = 0.01 * x_nodes[:, 0] ** 3  # Small displacement in x

    model.update_elements(U)

    f_int = model.internal_forces(U)
    f_vol = model.volumetric_forces(t=1.0)

    fig, ax = plt.subplots()
    mf.mesh.plot_mesh(mesh, ax, nodes_ids=True, elems_ids=True, zoom_out=0.25)

    ax = mf.post.fields.plot_2d_arrows(model.get_nodes_coordinates(), U, ax=ax, label='Displacement', color='C0')

    ax = mf.post.fields.plot_2d_arrows(model.get_nodes_coordinates(), f_vol, ax=ax, label='Volumetric Forces', color='C1')

    ax = mf.post.fields.plot_2d_arrows(model.get_nodes_coordinates(), f_int, ax=ax, label='Internal Forces', color='C2')

    ax.axis('off')
    ax.legend(loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.15))

    print("\nDisplaying mesh with displacement, volumetric forces, and internal forces...")
    plt.show()

    norm_fvol = []
    for t in np.linspace(0, 2.0, 21):
        Fvol = model.volumetric_forces(t)
        norm_fvol.append(np.linalg.norm(Fvol))

    fig, ax = plt.subplots()
    ax.plot(np.linspace(0, 2.0, 21), norm_fvol,'-o')
    ax.set_xlabel("Time")
    ax.set_ylabel("Norm of Volumetric Forces")
    ax.set_title("Norm of Volumetric Forces over Time")
    ax.grid(True)

    print("\nDisplaying norm of volumetric forces over time...")
    plt.show()

    fig, ax = plt.subplots()
    mf.mesh.plot_mesh(mesh, ax, nodes_ids=False, elems_ids=False)

    mf.post.fields.plot_2d_field(model.get_nodes_coordinates(), U, ax=ax, component="Mag", label='Displacement Magnitude')

    plt.show()

    x_nodes, sigma_avg = model.sigma(U)

    fig, ax = plt.subplots()
    mf.mesh.plot_mesh(mesh, ax, nodes_ids=False, elems_ids=False)

    mf.post.fields.plot_2d_field(x_nodes, sigma_avg, ax=ax, component="VM", label='VM Stress')

    plt.show()

    R = model.residual(U)
    print(f"\nResidual vector shape: {R.shape}, should be ({mesh.n_nodes}, {mesh.dim})")
    print(f"Residual vector norm: {np.linalg.norm(R)}")

    print("\n\nModel test completed successfully.")
