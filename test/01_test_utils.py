import numpy as np

import MecFEM.utils.stress as stress
import MecFEM.utils.kinematics as kinematics
import MecFEM.geometry.isoparametric_elements as ref
import MecFEM as mf

def test():
    material = mf.materials.non_linear.StVenantKirchhoffElasticity(E=200.0, nu=0.3)

    mesh = mf.mesh.Mesh("mesh/rect.msh", dim=2)
    element = mesh.get_element_by_id(100, 2)
    x_nodes = mesh.get_nodes_coordinates_by_element(100, 2)

    int_pts = ref.ReferenceElements().get_by_type(element.type).integration_points
    dim = element.dim

    fe = mf.elements.NonLinearFiniteElement(
        element,
        x_nodes,
    )

    stiffness, pk1_mat, grad0_u = fe.update(
        material,
        np.array([[0.05, 0.1], [0.1, 0.2], [0.15, 0.25], [0.2, 0.3]])
    )
    sigma_mat = material.sigma(grad0_u)
    tau_mat = material.tau(grad0_u)
    pk2_mat = material.pk2(grad0_u)

    F_mat = material.transformation_gradient(grad0_u)

    tau_sigma = stress.sigma2tau(sigma_mat, F_mat)
    pk1_sigma = stress.sigma2pk1(sigma_mat, F_mat)
    pk2_sigma = stress.sigma2pk2(sigma_mat, F_mat)

    sigma_tau = stress.tau2sigma(tau_mat, F_mat)
    pk1_tau = stress.tau2pk1(tau_mat, F_mat)
    pk2_tau = stress.tau2pk2(tau_mat, F_mat)

    sigma_pk1 = stress.pk12sigma(pk1_mat, F_mat)
    tau_pk1 = stress.pk12tau(pk1_mat, F_mat)
    pk2_pk1 = stress.pk12pk2(pk1_mat, F_mat)

    sigma_pk2 = stress.pk22sigma(pk2_mat, F_mat)
    tau_pk2 = stress.pk22tau(pk2_mat, F_mat)
    pk1_pk2 = stress.pk22pk1(pk2_mat, F_mat)

    # Verify dimensions
    assert pk1_mat.shape == (int_pts.N, dim, dim)
    assert sigma_mat.shape == (int_pts.N, dim, dim)
    assert tau_mat.shape == (int_pts.N, dim, dim)
    assert pk2_mat.shape == (int_pts.N, dim, dim)
    
    assert tau_sigma.shape == (int_pts.N, dim, dim)
    assert pk1_sigma.shape == (int_pts.N, dim, dim)
    assert pk2_sigma.shape == (int_pts.N, dim, dim)
    
    assert sigma_tau.shape == (int_pts.N, dim, dim)
    assert pk1_tau.shape == (int_pts.N, dim, dim)
    assert pk2_tau.shape == (int_pts.N, dim, dim)

    assert sigma_pk1.shape == (int_pts.N, dim, dim)
    assert tau_pk1.shape == (int_pts.N, dim, dim)
    assert pk2_pk1.shape == (int_pts.N, dim, dim)

    assert sigma_pk2.shape == (int_pts.N, dim, dim)
    assert tau_pk2.shape == (int_pts.N, dim, dim)
    assert pk1_pk2.shape == (int_pts.N, dim, dim)

    # Verify consistency
    assert np.allclose(pk1_mat, pk1_sigma)
    assert np.allclose(pk1_mat, pk1_tau)
    assert np.allclose(pk1_mat, pk1_pk2)

    assert np.allclose(sigma_mat, sigma_tau)
    assert np.allclose(sigma_mat, sigma_pk1)
    assert np.allclose(sigma_mat, sigma_pk2)

    assert np.allclose(tau_mat, tau_sigma)
    assert np.allclose(tau_mat, tau_pk1)
    assert np.allclose(tau_mat, tau_pk2)

    assert np.allclose(pk2_mat, pk2_sigma)
    assert np.allclose(pk2_mat, pk2_tau)
    assert np.allclose(pk2_mat, pk2_pk1)

    print("\n\nUtils test completed successfully.")

if __name__ == "__main__":
    test()
