import MecFEM as mf
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "figure.figsize": (10, 8),
    "figure.titlesize": 24,
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

if __name__ == "__main__":
    # mf.mesh.generate.generate_rectangle_mesh(
    #     2.0, 1.0, 10, 5, "mesh/rect.msh"
    # )

    # mesh = mf.mesh.read.read_gmsh_mesh("mesh/rect.msh", dim=2)

    # fig, ax = plt.subplots()
    # mf.mesh.plot_mesh(mesh, ax, nodes_ids=False, elems_ids=True)
    # plt.show()

    grad0_u = np.array(
        [
            [[0.1, 0.2], [0.0, 0.3]],
            [[0.0, 0.1], [0.2, 0.0]]
        ]
    )

    material = mf.materials.IsotropicElasticity(E=200.0, nu=0.3)

    # eps = material.epsilon(grad0_u)
    # F = material.deformation_gradient(grad0_u)
    # print("Strain tensor:")
    # print(eps)
    # print("Deformation gradient:")
    # print(F)

    # sigma = material.sigma(grad0_u)
    # print("Cauchy stress tensor:")
    # print(sigma)
    # tau = material.tau(grad0_u)
    # print("Kirchhoff stress tensor:")
    # print(tau)
    # P = material.pk1(grad0_u)
    # print("First Piola-Kirchhoff stress tensor:")
    # print(P)
    # S = material.pk2(grad0_u)
    # print("Second Piola-Kirchhoff stress tensor:")
    # print(S)

    # sigma_vm = mf.utils.stress.von_mises(sigma)
    # print(f"Von Mises stress: {sigma_vm}")

    # C = material.cauchy_green_right(F)
    # print("Right Cauchy-Green deformation tensor:")
    # print(C)
    # b = material.cauchy_green_left(F)
    # print("Left Cauchy-Green deformation tensor:")
    # print(b)
    # E = material.green_lagrange(F)
    # print("Green-Lagrange strain tensor:")
    # print(E)
    # e = material.euler_almansi(F)
    # print("Euler-Almansi strain tensor:")
    # print(e)

    elem_ref = mf.geometry.QUAD4()
    int_pts = mf.geometry.IPGauss2D(4)
    xNod = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
    dim = 2

    fe = mf.element.NonLinearFiniteElement(
        elem_ref,
        int_pts,
        xNod,
        dim
    )
    fe.update(
        np.array([[0.05, 0.1], [0.1, 0.2], [0.15, 0.25], [0.2, 0.3]]), 
        material
    )
    f_vol = fe.volumetric_force(
        np.random.rand(*xNod.shape)
    )
    print("Volumetric force vector:")
    print(f_vol)
    f_ext = fe.external_force(
        np.random.rand(*xNod.shape)
    )
    print("External force vector:")
    print(f_ext)




    