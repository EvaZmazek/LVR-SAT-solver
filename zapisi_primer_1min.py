from graphColouring import *

file = open("testni_primer_1min.txt", 'w')

G = [[1], [0, 1], [3, 5], [0, 4], [0, 3, 4], [2, 5, 7], [1, 2, 3]] 
# [[1,2,5,3,8,9], [0,2,3], [0,1,3,5,8], [0,1,2,4], [3,5,7,8,9], [0,2,6], [7,8,9], [5,6,8], [0,2,5,6,7], [0,5,6]]

formula = graphColouring2SATdo9(G, 3)
print(formula)
clauses = formula.terms

file.write("c testni_primer_1min.txt \n")
file.write("c barvanje grafa " + str(G) + "\n")
file.write("p cnf nekaj nekaj")
for clause in clauses:
    file.write("\n")
    zapisi = ""
    literals = clause.terms
    for literal in literals:
        if isinstance(literal, Variable):
            zapisi += str(literal)
            zapisi += " "
        elif isinstance(literal, Not):
            zapisi += "-"
            zapisi += str(literal.x)
            zapisi += " "
    zapisi += "0"
    file.write(zapisi)
