# MecFem

> **Status:**
>
> - *MecFEM*: Working, but features to be added
> - *app*: in development

## Next steps

- Add external forces to the solvers (*limited to volumetric with no spacial dependence for now*)
- Add tangent matrices for external and volumetric forces to the non-linear solver (*currently only the internal forces are considered in the tangent matrix*)
- Validation of solver (*done partially, but more cases to be analyzed*)
- Add sparse matrix compatibility to the solvers (*currently using dense matrices, which is not efficient for large problems*)
- Add support for 3d problems in the post-processing (*currently only 2d problems are supported*) --> Possibly PyVista although it is not yet supported in Flet
- Add commands for each boundary condition (simplify the application of boundary conditions in the app and in the examples)
- Finish the app (currently waiting for Matplotlib to be supported in Flet - [bug reported in Flet repo](https://github.com/flet-dev/flet/issues/6155))
- Finish documentation

## Summary

Finite element solver for mechanical problems. The code allows to solve up to 3D problems (although the post-processing is currently limited to 2D problems) and includes a GUI built with Flet for easy interaction.

There are two main solvers:

- **Linear**: Solves a linear system, where the stiffness matrix is constant and loads can be applied.
- **Non-linear**: Solves a non-linear system using the Newton-Raphson method, where the residual and tangent matrix depends on the current solution and the load is applied in increments.

## Directories Structure

- `src/MecFEM/` - Core finite element library
- `app/` - GUI application built with Flet
- `examples/` - Example scripts demonstrating how to use the MecFEM library
- `test/` - Some tests for MecFEM library
- `docs/` - Documentation files. A pdf with the documentation is also available in the root of the repository.

## Installation

### Clone the repository

```bash
git clone https://github.com/GabrielJezler/MecFem.git
cd MecFem
```

### Run flet app

- Install MecFEM as editable package (in the root of the repository)

```bash
pip install -e .
```

- Run the app

```bash
cd app
flet run
```
