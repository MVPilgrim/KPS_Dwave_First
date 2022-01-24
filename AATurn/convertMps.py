
import sys

from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler

import numpy  as numpy
import scipy  as sp
import pandas as pd


def parse_mps(data_file):
    callRows = False
    callColumnss = False
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
            if line == "COLUMNS":
                callColumnss = True
            elif callCols:
                processColumns(line)
             if line == "RHS":
                callRhs = True
            elif callRhs:
                processRhs(line)
             if line == "BOUNDS":
                callBounds = True
            elif callBounds:
                processBounds(line)
            elif line == "ENDATA"
                print("End of file.")

def processRows(line):
    print("processRows line: ",line)

def processColumns(line):
    print("processColumns line: ",line)

def processRhs(line):
    print("processRhs line: ",line)

def processBounds(line):
    print("processBounds line: ",line)

def main(argv):
    if not argv:
        filename = "LPWikiPediaExample.mps"
    else:
        filename = argv[0]
    print("filename: ",filename)
    parse_mps(filename)
    

if __name__ == '__main__':
    main(sys.argv[1:])
