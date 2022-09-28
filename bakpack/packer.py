from ortools.linear_solver import pywraplp
from typing import Union


def binpack(capacity: int, weights: list) -> Union[None, list[list[int]]]:
    """Pack widgets into minimum number of bins

    capacity is the size of a bin
    weights is a list of widget sizes

    returns the weights arranged in separate lists,
      each summing to no more than capacity
    """
    n_widgets = len(weights)
    # We allow for one bin per item so as to cover all solvable cases
    n_bins = n_widgets

    # After https://developers.google.com/optimization/bin/bin_packing#python_7

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SCIP")

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = dict(
        ((i, j), solver.IntVar(0, 1, f"x_{i}_{j}"))
        for i in range(n_widgets)
        for j in range(n_widgets)
    )

    # y[j] = 1 if bin j is used.
    y = dict((j, solver.IntVar(0, 1, f"y[{j}]")) for j in range(n_bins))

    # Constraints
    # Each item must be in exactly one bin.
    for i in range(n_widgets):
        solver.Add(sum(x[i, j] for j in range(n_bins)) == 1)

    # The amount packed in each bin cannot exceed its capacity.
    for j in range(n_bins):
        solver.Add(
            sum(x[i, j] * weights[i] for i in range(n_widgets)) <= y[j] * capacity
        )

    # Objective: minimize the number of bins used.
    solver.Minimize(solver.Sum([y[j] for j in range(n_bins)]))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        # print('Time = ', solver.WallTime(), ' milliseconds')
        bin_item_weights = []
        for j in range(n_bins):
            if y[j].solution_value() == 1:
                bin_item_weights.append(
                    sorted(
                        (
                            weights[i]
                            for i in range(n_widgets)
                            if x[i, j].solution_value() > 0
                        ),
                        reverse=True,
                    )
                )
        bin_item_weights.sort(reverse=True)
        # print(f"bin contents {bin_item_weights}")
        return bin_item_weights
    else:
        # print('The problem does not have an optimal solution.')
        return None
