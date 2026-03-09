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

def test():
    mf.mesh.generate.generate_rectangle_mesh(
        1.0, 0.5, 16, 8, "mesh/rect.msh"
    )
    
    mesh = mf.mesh.Mesh("mesh/rect.msh", dim=2)

    material = mf.materials.linear.IsotropicElasticity(E=200.0e9, nu=0.3)

    model = mf.models.Linear(
        mesh,
        material
    )

    x_nodes = mesh.get_nodes_coordinates()

    left_nodes = np.where(x_nodes[:, 0] == 0.0)[0]
    right_nodes = np.where(x_nodes[:, 0] == 1.0)[0]

    fix_disp_step = mf.boundary_conditions.functions.displacement.Fixed1Dof()
    x_disp_step = mf.boundary_conditions.functions.displacement.Displacement1Dof(mag=0.001)

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

    f = mf.boundary_conditions.functions.volumetric.Gravity(g=np.array([0.0, -9.81 * 1e4]), rho=1e3)

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
