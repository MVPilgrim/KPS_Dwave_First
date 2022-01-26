
import sys

from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler

import numpy  as numpy
import scipy  as sp
import pandas as pd


def parse_mps(data_file):
    callRows    = False
    callColumns = False
    callRhs     = False
    callBounds  = False

    with open(data_file) as f:
        for line in f:
            line = line.replace("\n","")
            print(line)
            if line == "ROWS":
                callRows = True
                continue
            if line == "COLUMNS":
                callRows = False
                callColumns = True
                continue
            if line == "RHS":
                callColumns = False
                callRhs = True
                continue
            if line == "BOUNDS":
                callRhs = False
                callBounds = True
                continue
            elif callRows:
                processRows(line)
            elif callColumns:
                processColumns(line)
            elif callRhs:
                processRhs(line)
            elif callBounds:
                processBounds(line)
            elif line == "ENDATA":
                callBounds = False
                print("End of file.")

def processRows(line):
    print("processRows line: ",line)
    leConstraintNames = []
    wl = line.split(" ")

    if wl[1] == 'N':
        objFuncName = wl[3]
        print("processRows() objFuncName: ",objFuncName)
    elif wl[1] == 'L':
        leConstraintNames.append(wl[3])
        print(leConstraintNames)

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
