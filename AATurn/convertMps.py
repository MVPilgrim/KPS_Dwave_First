
import sys

from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler

import numpy  as numpy
import scipy  as sp
import pandas as pd


objFuncName = ""
objFuncVarNamesAndCoeffs = {}
leConstraintNames = []
geConstraintNames = []
eqConstraintNames = []


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
    wl = line.split(" ")

    if wl[1] == 'N':
        objFuncName = wl[3]
        print("processRows() objFuncName: ",objFuncName)
    elif wl[1] == 'L':
        leConstraintNames.append(wl[3])
        print(leConstraintNames)
    elif wl[1] == 'G':
        geConstraintNames.append(wl[3])
        print(leConstraintNames)
    elif wl[1] == 'E':
        eqConstraintNames.append(wl[3])
        print(leConstraintNames)
    else:
        print("Invalid ROW type: ", wl[1])

def processColumns(line):
    print("processColumns() line: ",line)
    wl = line.split()
    print("processColumns() wl ",wl)

    if wl[1] == 'COST':
        objFuncVarNamesAndCoeffs[wl[0]] = wl[2]
        print("processColumns() objFuncVarNamesAndCoeffs: ",objFuncVarNamesAndCoeffs)
    else:
        print("Invalid COLUMN type: ", wl)

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
