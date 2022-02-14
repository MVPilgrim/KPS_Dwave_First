
import sys

from dimod import ConstrainedQuadraticModel, Integer
from dwave.system import LeapHybridCQMSampler

import numpy  as numpy

import scipy  as sp
import pandas as pd



objFuncVarNamesAndCoeffs   = {}

allConstraintNamesAndLists = {}

rhsConstraintsAndValues    = {}

upBoundsAndValues          = {}
loBoundsAndValues          = {}

objectiveFunction = "fdsa"


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
            elif line == "ENDATA":
                callBounds = False
                processEndata()
            elif callRows:
                processRows(line)
            elif callColumns:
                processColumns(line)
            elif callRhs:
                processRhs(line)
            elif callBounds:
                processBounds(line)
            

def addConstraintVal(constraintName,varName,val):
    # Map: constraint name and corresponding array: [constraint type,[[var name,value]]]
    ws = allConstraintNamesAndLists.get(constraintName,"xxx")
    if ws != "xxx":
        varvalList = ws + [[varName,val]]
        allConstraintNamesAndLists[constraintName] = varvalList
    else:
        print("addConstraintVal(): constraintName not in all constraints: ",constraintName)

def processRows(line):
    wl = line.split()

    if wl[0] == 'N':
        #print("first objectiveFunction ref: ",objectiveFunction)
        objectiveFunction = wl[1]
        print("objectiveFunction,wl[1]: ",objectiveFunction,",",wl[1])
    else:
        #allConstraintNamesAndLists = {wl[1]:[]}
        print("allConstraintNamesAndLists: ",allConstraintNamesAndLists)
        allConstraintNamesAndLists[wl[1]] = [wl[0]]

def processColumns(line):
    wl = line.split()

    if wl[1] == 'COST':
        # wl: dvarName[0],"COST"[1],val[2][,Constraint name[3], constraint val[4]]
        objFuncVarNamesAndCoeffs[wl[0]] = wl[2]
        if len(wl) == 5: 
            try:
                addConstraintVal(wl[3],wl[0],wl[4])
            except:
                print("processColumns() addConstraintVal(wl[3],wl[0],wl[4]): EXCEPT")
    elif wl[1] != "":
        addConstraintVal(wl[1],wl[0],wl[2])
    else:
        print("Invalid COLUMN type: ", wl)

def processRhs(line):
    wl = line.split()

    rhsConstraintsAndValues[wl[1]] = wl[2]

    if len(wl) == 5: 
        try:
            rhsConstraintsAndValues[wl[3]] = wl[4]
        except:
            print("processRhs() rhsConstraintsAndValues[wl[3]] = wl[4]: EXCEPT")


def processBounds(line):
    wl = line.split()

    # [constraint type,[[var name,value]]]
    if wl[0] == 'UP':
        if upBoundsAndValues.__len__() <= 0:
            upVars = ["UP"]
        else:
            upVars = list(upBoundsAndValues[wl[1]])
        upBoundsAndValues[wl[1]] = upVars + [[wl[2],wl[3]]]
    elif wl[0] == 'LO':
        if loBoundsAndValues.__len__() <= 0:
            loVars = ["LO"]
        else:
            loVars = list(upBoundsAndValues[wl[1]])
        loBoundsAndValues[wl[1]] = loVars + [[wl[2],wl[3]]]
    else:
        print("Invalid BOUNDS type: ", wl)
    
def processEndata():
    print("\nEnd of file.")
    print("obj func name: ",objectiveFunction)
    print("objFuncVarNamesAndCoeffs: ",objFuncVarNamesAndCoeffs)
    print("allConstraintNamesAndLists: ",allConstraintNamesAndLists)
    print("rhsConstraintsAndValues: ",rhsConstraintsAndValues)
    print("upBoundsAndValues: ",upBoundsAndValues)
    print("loBoundsAndValues: ",loBoundsAndValues)

def createLinprogInput():

    linprogObjFuncCoeffs = objFuncVarNamesAndCoeffs.values()
    allConstraintNamesAndLists
rhsConstraintsAndValues    = {}
upBoundsAndValues          = {}
loBoundsAndValues          = {}



def main(argv):
    if not argv:
        filename = "LPWikiPediaExample.mps"
    else:
        filename = argv[0]
    print("filename: ",filename)
    parse_mps(filename)

    createLinprogInput()
    

if __name__ == '__main__':
    main(sys.argv[1:])
