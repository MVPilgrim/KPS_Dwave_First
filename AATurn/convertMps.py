
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

linprogObjFuncCoeffs = []
linprogIneq = []
linprogEq   = []



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
    linprogIneq = []
    linprogEq   = []

    linprogObjFuncCoeffs = objFuncVarNamesAndCoeffs.values()
    # [constraint type,[[var name,value]]]
    for value in allConstraintNamesAndLists.values():
        print("value: ",value)
        if value[0] == "L":
            for value2 in value[1:]:
                print("Lvalue2: ",value2)
                #linprogIneq = linprogIneq + list(value2[1])
                linprogIneq.append(int(value2[1]))
        elif value[0] == "G":
            for value2 in value[1:]:
                print("Gvalue2: ",value2)
                coeff = int(value2[1]) * -1
                print("Gcoeff: ",coeff)
                #linprogIneq = linprogIneq + list(str(coeff))
                linprogIneq.append(coeff)
        elif value[0] == "E":
            for value2 in value[1:]:
                print("Evalue2: ",value2)
                #linprogEq = linprogEq + list(value2[1])
                linprogEq.append(int(value2[1]))
        else:
            print("createLinprogInput(): invalid constraint type: ",value[0])


    print("linprogIneq: ",linprogIneq)
    print("linprogEq: ",linprogEq)

def runLinprog():
    #opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
... #              A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
... #              method="revised simplex")


opt = linprog(c=linprogObjFuncCoeffs, A_ub=linprogIneq, b_ub=rhs_ineq,
...               A_eq=linprogEq, b_eq=rhs_eq, bounds=bnd,
...               method="revised simplex")

def main(argv):
    if not argv:
        filename = "LPWikiPediaExample.mps"
    else:
        filename = argv[0]
    print("filename: ",filename)
    parse_mps(filename)

    createLinprogInput()
    runLinprog()

if __name__ == '__main__':
    main(sys.argv[1:])
