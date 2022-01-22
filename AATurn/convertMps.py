
from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler
import pandas as pd


def parse_inputs(data_file):
    df = pd.read_csv(data_file, names=['cost'])

    return df['cost']



def main(argv):

    filename = argv[1]
    print("filename: ",filename)
    

if __name__ == '__main__':
    main(sys.argv)
