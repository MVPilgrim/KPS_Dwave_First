
import sys

from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler

import numpy  as numpy

import scipy  as sp
import pandas as pd


objFuncName = ""
objFuncVarNamesAndCoeffs   = {}

allConstraintNamesAndLists  = {}

leConstraintNamesAndCoeffs = {}
leConstraintNamesAndRHS    = {}

eqConstraintNamesAndCoeffs = {}
eqConstraintNamesAndRHS    = {}

geConstraintNamesAndCoeffs = {}
geConstraintNamesAndRHS    = {}


def parse_mps(data_file):
    callRows    = False
    callColumns = False
    callRhs     = False
    callBounds  = False

    with open(data_file) as f:
        for line in f:
            line = line.replace("\n","")
            print("Input line: ",line)
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

def addConstraintVal(constraintName,varName,val):
    # Map: constraint name and corresponding array: [constraint type,[[var name,value]]]
    ws = allConstraintNamesAndLists.get(constraintName,"xxx")
    if ws != "xxx":
        varvalList = ws[0,0]
        print("varvalLIst: ",varvalList)
    else:
        print("addConstraintVal(): constraintName not in all constraints: ",constraintName)

def processRows(line):
    print("processRows line: ",line)
    wl = line.split()

    if wl[0] == 'N':
        objFuncName = wl[1]
        #print("processRows() objFuncName: ",objFuncName)
    elif wl[0] == 'L':
        allConstraintNamesAndLists = {wl[1]:[]}
        print("allConstraintNamesAndLists: ",allConstraintNamesAndLists)
    elif wl[0] == 'G':
        x=0
    elif wl[0] == 'E':
        x=0
    else:
        print("Invalid ROW type: ", wl[1])

def processColumns(line):
    print("processColumns() line: ",line)
    wl = line.split()
    print("processColumns() array: ",wl)

    if wl[1] == 'COST':
        # wl: dvarName[0],"COST"[1],val[2][,Constraint name[3], constraint val[4]]
        objFuncVarNamesAndCoeffs[wl[0]] = wl[2]
        print("ProcessColumns(): wl.count(): ",len(wl))
        if len(wl) == 5: 
            try:
                addConstraintVal(wl[3],wl[0],wl[4])
                print("processColumns() objFuncVarNamesAndCoeffs: ",objFuncVarNamesAndCoeffs)
            except:
                print("processColumns() objFuncVarNamesAndCoeffs: EXCEPT")
    elif wl[1] != "":
        xxx = 1
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
