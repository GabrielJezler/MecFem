import gmsh

def generate_1d_line_mesh(n, x0=0.0, x1=1.0, order=1, filename="mesh\\line.msh"):
    # Initialize the Gmsh API
    gmsh.initialize()

    # Set the model name
    gmsh.model.add("1D Line")

    # Define the start and end points of the line
    p1 = gmsh.model.geo.addPoint(x0, 0, 0, 1.0)  # Start point
    p2 = gmsh.model.geo.addPoint(x1, 0, 0, 1.0)  # End point

    # Define the line connecting the points
    line = gmsh.model.geo.addLine(p1, p2)

    # Synchronize the CAD representation
    gmsh.model.geo.synchronize()

    # Specify the number of nodes for the line mesh
    gmsh.model.mesh.setTransfiniteCurve(line, n)  # n nodes, n-1 segments

    # Select order
    gmsh.option.setNumber("Mesh.ElementOrder", order)

    # Generate the mesh
    gmsh.model.mesh.generate(1)  # 1D mesh

    # Save the mesh to a file
    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
    gmsh.write(filename)
    
    # Finalize the Gmsh API
    gmsh.finalize()

    return filename

def generate_rectangle_mesh(a, b, nx, ny, filename="mesh\\rectangle.msh"):
    """
    Generate a rectangle with dimensions a x b and a structured quad4 mesh
    with element sizes dx and dy.

    Parameters:
        a (float): Length of the rectangle along the x-axis.
        b (float): Length of the rectangle along the y-axis.
        nx (int): Number of nodes along the x-axis.
        ny (int): Number of nodes along the y-axis.
    """
    # Initialize the Gmsh API
    gmsh.initialize()

    # Set the model name
    gmsh.model.add("Rectangle")

    # Define corner points of the rectangle
    p1 = gmsh.model.geo.addPoint(0, 0, 0, 1.0)  # Bottom-left corner
    p2 = gmsh.model.geo.addPoint(a, 0, 0, 1.0)  # Bottom-right corner
    p3 = gmsh.model.geo.addPoint(a, b, 0, 1.0)  # Top-right corner
    p4 = gmsh.model.geo.addPoint(0, b, 0, 1.0)  # Top-left corner

    # Define the rectangle edges
    l1 = gmsh.model.geo.addLine(p1, p2)  # Bottom edge
    l2 = gmsh.model.geo.addLine(p2, p3)  # Right edge
    l3 = gmsh.model.geo.addLine(p3, p4)  # Top edge
    l4 = gmsh.model.geo.addLine(p4, p1)  # Left edge

    # Create a curve loop and a plane surface
    curve_loop = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
    surface = gmsh.model.geo.addPlaneSurface([curve_loop])

    # Synchronize the CAD representation
    gmsh.model.geo.synchronize()

    # Set transfinite meshing for structured quads
    gmsh.model.mesh.setTransfiniteCurve(l1, nx)  # Bottom edge
    gmsh.model.mesh.setTransfiniteCurve(l2, ny)  # Right edge
    gmsh.model.mesh.setTransfiniteCurve(l3, nx)  # Top edge
    gmsh.model.mesh.setTransfiniteCurve(l4, ny)  # Left edge
    gmsh.model.mesh.setTransfiniteSurface(surface)
    gmsh.model.mesh.setRecombine(2, surface)  # Recombine into quads

    # Generate the mesh
    gmsh.model.mesh.generate(2)  # 2D mesh

    # Save the mesh to a file
    gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
    gmsh.write(filename)

    # Finalize the Gmsh API
    gmsh.finalize()

    return filename

