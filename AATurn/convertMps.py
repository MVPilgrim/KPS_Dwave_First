
import sys

from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler

import numpy  as numpy
import scipy  as sp
import pandas as pd


def parse_mps(data_file):
    callRows = False
    callCols = False
    callRhs  = False
    callBounds = False

    with open(data_file) as f:
        for line in f:
            line = line.replace("\n","")
            print(line)
            if line == "ROWS":
                callRows = True
            elif callRows:
                processRows(line)
            if line == "COLS":
                callCols = True
            elif callCols:
                processCols(line)
             if line == "RHS":
                callRhs = True
            elif callRhs:
                processRhs(line)
             if line == "BOUNDS":
                callBounds = True
            elif callBounds:
                processBounds(line)
            elif line == "ENDATA"

def processRows(line):
    print("processRows line: ",line)

def main(argv):
    if not argv:
        filename = "LPWikiPediaExample.mps"
    else:
        filename = argv[0]
    print("filename: ",filename)
    parse_mps(filename)
    

if __name__ == '__main__':
    main(sys.argv[1:])
