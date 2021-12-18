
from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler
import pandas as pd


def parse_inputs(data_file):
    df = pd.read_csv(data_file, names=['cost'])

    return df['cost']


def build_cqm(f,e,b,s):
    
    print("\nBuilding the CQM.\n")

    cqm = ConstrainedQuadraticModel()

    cqm.set_objective((f + e + b + s) * -1)

    cqm.add_constraint(f + e + b + s == 700, "Total amt. in gredients")
    cqm.add_constraint(b - 0.5 * s == 0, "Reduce butter and sugar.")
    cqm.add_constraint(f + e <= 450, "Flour plus eggs.")
    cqm.add_constraint(e + b <= 300, "Eggs plus butter.")

    return cqm


def parse_solution(sampleset):
   
    feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)

    if not len(feasible_sampleset):
        raise ValueError("No feasible solution found")

    best = feasible_sampleset.first

    print("Found best solution at energy {}\n".format(best.energy))
    #print("Selected item numbers (0-indexed): \n", selected_item_indices)


def main():

    sampler = LeapHybridCQMSampler()

    filename = "cake.csv"
    #f, e, b, s = parse_inputs(filename)
    f = Integer('f')
    e = Integer('e')
    b = Integer('b')
    s = Integer('s')

    cqm = build_cqm(f,e,b,s)

    print("Submitting CQM to solver {}.".format(sampler.solver.name))
    sampleset = sampler.sample_cqm(cqm, label='Bake a Cake')

    parse_solution(sampleset)

if __name__ == '__main__':
    main()
