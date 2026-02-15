import numpy as np
import gmsh

import MecFEM.geometry.isoparametric_elements as ref

def evaluate_shape_functions(elem):
    """
    Test shape functions for an isoparametric element. It verifies that:
        - At each node, the corresponding shape function is 1 and all others are 0.
        - The sum of all shape functions at the nodes is 1.
        - At a random point inside the element, the sum of all shape functions is 1.

    Parameters
    ----------
    elem : ReferenceElement
        The reference element to test.
    """
    nodes = elem.nodes
    n_nodes = nodes.shape[0]

    gmsh.initialize()
    for i in range(n_nodes): # for each node
        N = elem.shape_function.shape(nodes[i])
        assert N.shape == (n_nodes, 1), f"Shape function output shape mismatch: expected {(n_nodes, 1)}, got {N.shape}"
        assert np.isclose(np.sum(N), 1.0), f"Sum of shape functions at node {i} should be 1, got {np.sum(N)}"

        for j in range(n_nodes): # for each shape function
            if i == j:
                assert np.isclose(N[j,0], 1.0), f"Shape function {j} at node {i} should be 1, got {N[j,0]}"
            else:
                assert np.isclose(N[j,0], 0.0), f"Shape function {j} at node {i} should be 0, got {N[j,0]}"

    gmsh.finalize()

    amplitude = np.max(nodes, axis=0) - np.min(nodes, axis=0)
    CG = np.mean(nodes, axis=0)
    point = CG + amplitude * 0.1 * (np.random.rand(*amplitude.shape) - 0.5)

    N = elem.shape_function.shape(point)
    assert N.shape == (n_nodes, 1), f"Shape function output shape mismatch at random point: expected {(n_nodes, 1)}, got {N.shape}"
    assert np.isclose(np.sum(N), 1.0), f"Sum of shape functions at random point should be 1, got {np.sum(N)}"

def evaluate_dShape_functions(elem):
    """
    Test derivatives of shape functions for an isoparametric element. It verifies that:
        - The sum of the derivatives of all shape functions with respect to each coordinate should be zero.

    Parameters
    ----------
    elem : ReferenceElement
        The reference element to test.
    """
    nodes = elem.nodes
    n_nodes = nodes.shape[0]
    n_dim = nodes.shape[1]

    for i in range(n_nodes): # for each node
        dN = elem.shape_function.dShape(nodes[i])  # shape (n_nodes, n_dim)
        assert dN.shape == (n_nodes, n_dim), f"dShape function output shape mismatch: expected {(n_nodes, n_dim)}, got {dN.shape}"
        for dim in range(n_dim):
            sum_dN = np.sum(dN[:, dim])
            assert np.isclose(sum_dN, 0.0), f"Sum of derivatives w.r.t. dimension {dim} at node {i} should be 0, got {sum_dN}"

    amplitude = np.max(nodes, axis=0) - np.min(nodes, axis=0)
    CG = np.mean(nodes, axis=0)
    point = CG + amplitude * 0.1 * (np.random.rand(*amplitude.shape) - 0.5)

    dN = elem.shape_function.dShape(point)
    assert dN.shape == (n_nodes, n_dim), f"dShape function output shape mismatch at random point: expected {(n_nodes, n_dim)}, got {dN.shape}"
    for dim in range(n_dim):
        sum_dN = np.sum(dN[:, dim])
        assert np.isclose(sum_dN, 0.0), f"Sum of derivatives w.r.t. dimension {dim} at random point should be 0, got {sum_dN}"

def test():
    for element in ref.ReferenceElements.ELEMS:
        print(f"Testing element: {element.name}")

        evaluate_shape_functions(element)
        print(f"    Shape function:               SUCCESS")

        evaluate_dShape_functions(element)
        print(f"    Derivative of shape function: SUCCESS")


    print("\n\nShape function test completed successfully.")

if __name__ == "__main__":
    test()
