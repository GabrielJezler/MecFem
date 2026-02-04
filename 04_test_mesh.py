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

if __name__ == "__main__":
    mf.mesh.generate.generate_rectangle_mesh(
        2.0, 1.0, 10, 5, "mesh/rect.msh"
    )

    mesh = mf.mesh.read.read_gmsh_mesh("mesh/rect.msh", dim=2)

    fig, ax = plt.subplots()
    mf.mesh.plot_mesh(mesh, ax, nodes_ids=True, elems_ids=True)
    plt.show()

    mf.mesh.generate.generate_1d_line_mesh(
        10, 0.0, 1.0, filename="mesh/line.msh"
    )
    
    mesh = mf.mesh.read.read_gmsh_mesh("mesh/line.msh", dim=1)

    fig, ax = plt.subplots()
    mf.mesh.plot_mesh(mesh, ax, nodes_ids=False, elems_ids=True)
    plt.show()
    
    print("\n\nMesh test completed successfully.")
