import copy
from boolean import *
from dpll_algoritem import *
import sys
import time

sys.setrecursionlimit(2000)

file1 = open(sys.argv[1], 'r')
file2 = open(sys.argv[2], 'w')

clauses = []

for line in file1:
    if line[0]=="c":
        continue
    elif line[0]== "p":
        arguments = line.strip().split(" ")
        st_variables = arguments[2]
        st_clauses = arguments[3]
    else:
        list_line = line.strip().split(" ")
        list_line = list_line[:-1]
        literals = []
        for element in list_line:
            if element[0]=="-":
                literals.append(Not(element[1:]))
            else:
                literals.append(element)
        clause = Or(*literals)
        clauses.append(clause)

unsatisfiable = "formula is unsatisfiable"
f = And(*clauses)
##print(f)
ff = copy.deepcopy(f)

start = time.time()
valuation = my_dpll(f)
##print(valuation)
end = time.time()
print(end-start)

if valuation == unsatisfiable:
    file2.write("0")
else:
##    print(ff.evaluate(valuation))
    resitev = ""
    for i in valuation:
        resitev += " "
        if valuation[i]:
            resitev += str(i)
        else:
            resitev += "-"
            resitev += str(i)
    file2.write(resitev)
