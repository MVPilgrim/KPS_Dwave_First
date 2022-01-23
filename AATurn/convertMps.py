
import sys

from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler

import numpy  as numpy
import scipy  as sp
import pandas as pd


def parse_mps(data_file):
    with open('workfile') as f:
        for line in f:
            if line != "":
            else:
                print("End of file")



def main(filename):
    print("filename: ",filename[0])
    parse_mps(filename[0])
    

if __name__ == '__main__':
    main(sys.argv[1:])
