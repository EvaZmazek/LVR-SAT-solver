from graphColouring import *

file = open("testni_primer_1min.txt", 'w')

G = [[1,5], [0,2], [1,3], [2,4], [3,5], [0,4]]

formula = graphColouring2SATdo9(G, 2)
formula2 = graphColouring2SAT(G,2)
print(formula)
print(formula2)
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
