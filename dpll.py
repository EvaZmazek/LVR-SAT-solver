from boolean import *

#predpostavljamo, da je formula podana v CNF obliki

def get_all_from_CNF(formula):
    if not isinstance(formula, And):
        return "formula ni podana v CNF obliki!"

def my_dpll(formula):
    valuation = dict()
    print(formula)
    if not isinstance(formula, And):
        return "formula ni podana v CNF obliki!"
    clauses = formula.terms
    print(clauses)
    #1. prazen seznam clausesov predstavlja vrednost T (satisfiable solution)
    if len(clauses)==0:
        return True
    #2. pregledamo, če je kateri izmed clausesov prazen, potem rešitve ni
    for clause in clauses:
        literals = clause.terms
        if len(literals) == 0:
            return False

def simplify_dpll(formula):
    pass

def simplify_unit_clause(formula, valuation):
    clauses = formula.terms
    for clause in clauses:
        if isinstance(clause, Or):
            literals = clause.terms
            if len(literals)==1:
                clause = literals[0]
            else:
                pass
        if isinstance(clause, Variable):
            valuation[clause.x]=True
        elif isinstance(clause, Not):
            if not isinstance(clause.x, Variable):
                print("formula ni podana v CNF obliki!")
            valuation[clause.x.x]=False
    return valuation
