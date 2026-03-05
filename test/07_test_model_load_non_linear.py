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

    material = mf.materials.non_linear.StVenantKirchhoffElasticity(E=200.0e9, nu=0.3)

    model = mf.models.NonLinear(
        mesh,
        material
    )

    model.load_gmsh_results(filename="mesh/rect_out.msh", U_values_name="Displacement")
    
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

    fig, ax = plt.subplots()
    ax = mesh.plot(ax=ax, nodes_marker=False, nodes_ids=False, elems_ids=False, zoom_out=0.25)

    ax = mf.post.vector.plot_2d_arrows(model, model.R[-1], ax=ax, scale=2e8, label='Reaction vectors')

    fig.suptitle("Reaction vectors")
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
