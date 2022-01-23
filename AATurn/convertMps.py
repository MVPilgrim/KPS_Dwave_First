
import sys

from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler

import numpy  as numpy
import scipy  as sp
import pandas as pd


def parse_mps(data_file):
    with open(data_file) as f:
        for line in f:
            print(line.replace("\n",""))



def main(argv):
    if not argv:
        filename = "LPWikiPediaExample.mps"
    else:
        filename = argv[0]
    print("filename: ",filename)
    parse_mps(filename)
    

if __name__ == '__main__':
    main(sys.argv[1:])
