
from dimod import ConstrainedQuadraticModel, Integer
import pandas

i = Integer('i', upper_bound=4)
j = Integer('j', upper_bound=4)
cqm = ConstrainedQuadraticModel()


def parse_inputs(data_file, capacity):
    """Parse user input and files for data to build CQM.

    Args:
        data_file (csv file):
            File of items (cost) slated to ship.

    Returns:
        Cost. fdsa
    """
    df = pd.read_csv(data_file, names=['cost'])

    return df['cost']


def build_cqm(costs, weights, max_weight):
    """Construct a CQM for the knapsack problem.

    Args:
        costs (array-like):
            Array of costs for the items.
        weights (array-like):
            Array of weights for the items.
        max_weight (int):
            Maximum allowable weight for the knapsack.

    Returns:
        Constrained quadratic model instance that represents the knapsack problem.
    """
    num_items = len(costs)
    print("\nBuilding a CQM for {} items.".format(str(num_items)))

    cqm = ConstrainedQuadraticModel()
    obj = BinaryQuadraticModel(vartype='BINARY')
    constraint = QuadraticModel()

    for i in range(num_items):
        # Objective is to maximize the total costs
        obj.add_variable(i)
        obj.set_linear(i, -costs[i])
        # Constraint is to keep the sum of items' weights under or equal capacity
        constraint.add_variable('BINARY', i)
        constraint.set_linear(i, weights[i])

    cqm.set_objective(obj)
    cqm.add_constraint(constraint, sense="<=", rhs=max_weight, label='capacity')

    return cqm


def parse_solution(sampleset, costs, weights):
    """Translate the best sample returned from solver to shipped items.

    Args:

        sampleset (dimod.Sampleset):
            Samples returned from the solver.
        costs (array-like):
            Array of costs for the items.
        weights (array-like):
            Array of weights for the items.
    """
    feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)

    if not len(feasible_sampleset):
        raise ValueError("No feasible solution found")

    best = feasible_sampleset.first

    selected_item_indices = [key for key, val in best.sample.items() if val==1.0]
    selected_weights = list(weights.loc[selected_item_indices])
    selected_costs = list(costs.loc[selected_item_indices])

    print("\nFound best solution at energy {}".format(best.energy))
    print("\nSelected item numbers (0-indexed):", selected_item_indices)
    print("\nSelected item weights: {}, total = {}".format(selected_weights, sum(selected_weights)))
    print("\nSelected item costs: {}, total = {}".format(selected_costs, sum(selected_costs)))


def main(filename, capacity):
    """Run cake recipe example to comare with cvxopt linprog() python example."""

    sampler = LeapHybridCQMSampler()

    costs, weights, capacity = parse_inputs(filename, capacity)

    cqm = build_knapsack_cqm(costs, weights, capacity)

    print("Submitting CQM to solver {}.".format(sampler.solver.name))
    sampleset = sampler.sample_cqm(cqm, label='Example - Knapsack')

    parse_solution(sampleset, costs, weights)

if __name__ == '__main__':
    main()
