
import sys
import numpy  as numpy
import scipy  as sp

#from dimod import ConstrainedQuadraticModel, Integer
#from dwave.system import LeapHybridCQMSampler
#import pandas as pd


objFuncVarNamesAndCoeffs   = {}
allConstraintNamesAndLists = {}

rhsConstraintsAndValues    = {}

upBoundsAndValues          = {}
loBoundsAndValues          = {}

objectiveFunction = "fdsa"

linprogObjFuncCoeffs = []

linprogLhsIneq = []
linprogLhsEq   = []

linprogRhsIneq = []
linprogRhsEq   = []

linprogBnds = []


def forDocstrings():
    """
    Map
    objFuncVarNamesAndCoeffs:  {'XONE': '1', 'YTWO': '4', 'ZTHREE': '9'}
      MPS file Columns: COST coeffs.
                                 XONE COST 1
                                              YTWO COST 4
                                                           ZTHREE COST 9
    
    Map with sublists.
    allConstraintNamesAndLists:  {'LIM1': ['L', ['XONE', '1'], ['YTWO', '1']], 'LIM2': ['G', ['XONE', '1'], ['ZTHREE', '1']], 'MYEQN': ['E', ['YTWO', '-1'], ['ZTHREE', '1']]}
      MPS file Columns 
        constraints coeffs.
        LIM1, LIM2, MYEQN
                                                  XONE    1
                                                                                               XONE    1
                                                                 YTWO    1
                                                                                                              ZTHREE    1 
                                                                                                                                              YTWO     -1
                                                                                                                                                              ZTHREE     1
    

    map
    rhsConstraintsAndValues:  {'LIM1': '5', 'LIM2': '10', 'MYEQN': '7'}
      MPS "RHS" entries         LIM1    5   
        LIM1, LIM2, MYEQN                    LIM2    10
                                                           MYEQN    7

    
    upBoundsAndValues:  {'BND1': ['UP', ['XONE', '4'], ['YTWO', '1']]}
      MPS upper limits on                 XONE    4                    
      variable values.                                   YTWO    1
    
    loBoundsAndValues:  {'BND1': ['LO', ['YTWO', '-1']]}
    MPS lower limits on                   YTWO    -1
      variable values.

    """

    x=0

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
    global objectiveFunction

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
            loVars = list(loBoundsAndValues[wl[1]])
        loBoundsAndValues[wl[1]] = loVars + [[wl[2],wl[3]]]
    else:
        print("Invalid BOUNDS type: ", wl)
    
def processEndata():
    """ processEndata() DOCSTRING."""
    print("\nEnd of file.")
    print("obj func name: ",objectiveFunction)
    print("objFuncVarNamesAndCoeffs: ",objFuncVarNamesAndCoeffs)
    print("allConstraintNamesAndLists: ",allConstraintNamesAndLists)
    print("rhsConstraintsAndValues: ",rhsConstraintsAndValues)
    print("upBoundsAndValues: ",upBoundsAndValues)
    print("loBoundsAndValues: ",loBoundsAndValues)


def createLinprogInput():
    global linprogObjFuncCoeffs
    global linprogRhs

    # Set left and right-hand sides of constraints.
    # Set list of cost coefficients.
    linprogObjFuncCoeffs = list(objFuncVarNamesAndCoeffs.values())
    
    # [constraint type,[[var name,value]]]
    for key in allConstraintNamesAndLists.keys():
        print ("key: ",key)
        value = allConstraintNamesAndLists.get(key)
        print("value: ",value)
        if value[0] == "L":
            wrkConstraintValues = []
            for value2 in value[1:]:
                print("Lvalue2: ",value2)
                wrkConstraintValues.append(int(value2[1]))
            rhsValue = rhsConstraintsAndValues.get(key)
            linprogRhsIneq.append(int(rhsValue))
            linprogLhsIneq.append(wrkConstraintValues)
        elif value[0] == "G":
            wrkConstraintValues = []
            for value2 in value[1:]:
                print("Gvalue2: ",value2)
                coeff = int(value2[1]) * -1
                print("Gcoeff: ",coeff)
                wrkConstraintValues.append(coeff)
            rhsValue = rhsConstraintsAndValues.get(key)
            linprogRhsIneq.append(int(rhsValue))
            linprogLhsIneq.append(wrkConstraintValues)
        elif value[0] == "E":
            for value2 in value[1:]:
                print("Evalue2: ",value2)
                #linprogLhsEq = linprogLhsEq + list(value2[1])
                linprogLhsEq.append(int(value2[1]))
            rhsValue = rhsConstraintsAndValues.get(key)
            linprogRhsEq.append(int(rhsValue))
        else:
            print("createLinprogInput(): invalid constraint type: ",value[0])

    # loBoundsAndValues:  {'BND1': ['LO', ['YTWO', '-1']]}
    # upBoundsAndValues:  {'BND1': ['UP', ['XONE', '4'], ['YTWO', '1']]}

    # Set bounds by processing cost variables in order.
    for costKey in objFuncVarNamesAndCoeffs.keys():
        loBnd = float("inf")
        upBnd = -float("inf")
        # Process lower bounds.
        loBndArray1 = loBoundsAndValues.values()
        print("loBndArray1: ",loBndArray1)
        for loBndArray2 in loBndArray1:
            print("loBndArray2: ",loBndArray2)
            #loBndArray2 = loBndArray2[1]
            loBndArray2 = list(loBndArray2)
            print("loBndArray2: ",loBndArray2)
            for loBndArray3 in loBndArray2:
                if loBndArray3[0] == costKey:
                    loBnd   = loBndArray3[1]
                    print("loBnd: ",loBnd)
                    #break
        # Process upper bounds.
        upBndArray1 = upBoundsAndValues.values()
        print("upBndArray1: ",upBndArray1)
        for upBndArray2 in upBndArray1:
            print("upBndArray2: ",upBndArray2)
            #upBndArray2 = upBndArray2[1]
            upBndArray2 = list(upBndArray2)
            print("upBndArray2: ",upBndArray2)
            for upBndArray3 in upBndArray2:
                if upBndArray3[0] == costKey:
                    upBnd   = upBndArray3[1]
                    print("upBnd: ",upBnd)
                    #break

        if not(loBnd == float("inf") and upBnd == -float("inf")):
            if loBnd == float("inf"):
                loBnd = int(0)
            if upBnd == -float("inf"):
                upBnd = float("inf")
            linprogBnds.append((loBnd,upBnd))

    print("linprogObjFuncCoeffs: ",linprogObjFuncCoeffs)
    print("linprogLhsIneq: ",linprogLhsIneq)
    print("linprogLhsEq: ",  linprogLhsEq)
    print("linprogRhsIneq: ", linprogRhsIneq)
    print("linprogRhsEq: ", linprogRhsEq)
    print("linprogBnds: ",linprogBnds)

def runLinprog():
    #opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq,
    #              A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd,
    #              method="revised simplex")


    #opt = linprog(c=linprogObjFuncCoeffs, A_ub=linprogLhsIneq, b_ub=rhs_ineq,
    #    A_eq=linprogLhsEq, b_eq=rhs_eq, bounds=bnd,
    #    method="revised simplex")

    x = 0

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
