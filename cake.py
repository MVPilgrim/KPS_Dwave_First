
from dimod import ConstrainedQuadraticModel, Integer
import pandas as pd


def parse_inputs(data_file, capacity):
    df = pd.read_csv(data_file, names=['cost'])

    return df['cost']


def build_cqm(costs):
    
    num_items = len(costs)
    print("\nBuilding a CQM for {} items.".format(str(num_items)))

    cqm = ConstrainedQuadraticModel()

    cqm.add_constraint(2*i+2*j <= 8, "Max perimeter")
    cqm.add_constraint(constraint, sense="<=", rhs=max_weight, label='capacity')

    return cqm


def parse_solution(sampleset, costs, weights):
   
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

    sampler = LeapHybridCQMSampler()

    costs, weights, capacity = parse_inputs(filename, capacity)

    cqm = build_cqm(costs)

    print("Submitting CQM to solver {}.".format(sampler.solver.name))
    sampleset = sampler.sample_cqm(cqm, label='Example - Knapsack')

    parse_solution(sampleset, costs, weights)

if __name__ == '__main__':
    main()
