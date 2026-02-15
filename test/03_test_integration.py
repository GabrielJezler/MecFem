import numpy as np
import matplotlib.pyplot as plt

import MecFEM.geometry.isoparametric_elements as ref

plt.rcParams.update({
    "figure.figsize": (10, 8),
    "figure.titlesize": 24,
    "axes.titlesize": 20,
    "font.family": "Courier New",
    "font.size": 16,
    "savefig.format": "pdf",
})

def plot_integration_points(elem:ref.ReferenceElementData, ax=None):
    if ax is None:
        fig, ax = plt.subplots(1, 3, figsize=(12,5))

    dim = elem.dim
    nodes = elem.nodes

    integration = elem.integration_points

    X = integration.X
    W = integration.W

    if dim == 1:
        ax.plot(nodes[:,0], np.zeros_like(nodes[:,0]), 'k-o', zorder=-10)
        sc = ax.scatter(X[:,0], np.zeros_like(X[:,0]), c=W, cmap='winter', s=100)
        plt.colorbar(sc, ax=ax, label='Weights', ticks=W)
        ax.set_title(f'N = {elem.integration_points.N}')
    
    elif dim == 2:
        ax.fill(nodes[:,0], nodes[:,1], facecolor='lightgray', edgecolor='k', alpha=1.0, zorder=-10)
        ax.scatter(nodes[:,0], nodes[:,1], c='k', zorder=-10)
        sc = ax.scatter(X[:,0], X[:,1], c=W, cmap='winter', s=100)
        plt.colorbar(sc, ax=ax, label='Weights', ticks=W)
        ax.set_title(f'N = {elem.integration_points.N}')

    ax.set_box_aspect(1)
    ax.set_aspect('equal')
    ax.axis('equal')
    ax.axis('off')


def test():
    for element in [ref.ReferenceElements().get_by_type(1), ref.ReferenceElements().get_by_type(2), ref.ReferenceElements().get_by_type(3)]:
        fig, ax = plt.subplots(1, 3, figsize=(15,5))
        for i in range(3):
            n = element.integration_points.possible_integration_numbers()
            if n is None:
                if element.type == 1:
                    n = i + 1
                elif element.type == 3:
                    n = (i+1)**2
            else:
                n = n[i]
            element.set_integration_number(n)
            plot_integration_points(element, ax=ax[i])

        fig.suptitle(f'Integration Points for Element: {element.name}')
        plt.show()
        
    print("\n\nIntegration test completed successfully.")

if __name__ == "__main__":
    test()
