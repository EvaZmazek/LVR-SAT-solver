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
    #TODO dodaj še spreminjanje spremenljivk glede na že znane vrednosti
    #TODO končaj program, če v slovar dodajaš drugačno vrednost, kot je že dodana
    print(formula)
    clauses = formula.terms
    for clause in clauses:
        if isinstance(clause, Or):
            literals = clause.terms
            if len(literals)==1:
                clauses.remove(clause)
                formula = And(*clauses)
                clause = literals[0]
                if isinstance(literals[0], Variable):
                    valuation[clause.x]=True
                elif isinstance(clause, Not):
                    if not isinstance(clause.x, Variable):
                        print("formula ni podana v CNF obliki!")
                    valuation[clause.x.x]=False
                simplify_unit_clause(formula, valuation)
                break
            else:
                continue
        elif isinstance(clause, Variable):
            valuation[clause.x]=True
            clauses.remove(clause)
            formula = And(*clauses)
            simplify_unit_clause(formula, valuation)
            break
        elif isinstance(clause, Not):
            if not isinstance(clause.x, Variable):
                print("formula ni podana v CNF obliki!")
            valuation[clause.x.x]=False
            clauses.remove(clause)
            formula = And(*clauses)
            simplify_unit_clause(formula, valuation)
            break
    return valuation

def simplify_pore_literal(formula, valuation):
    #mogoče pojdi čez seznam vseh spremenljivk in označi, če je spremenljivka (nastavi na true),
    #če je negacija (nastavi na false) in preglejuj če se kdaj seka --> odstrani iz seznama pure
    #pure literal. Na začetku nastavi na none
    pass

def simplify_by_literal(formula, l, tf):
    print(formula)
    clauses = formula.terms
    print(clauses)
    st_clauses = len(clauses)
    i = 0
    while i < st_clauses:
        clause = clauses[i]
        i = i+1
        if isinstance(clause, Or):
            literals = clause.terms
            if len(literals)==0:
                formula = F
                break
            elif tf:
                if l in literals:
                    clauses.remove(clause)
                    i, st_clauses = i-1, st_clauses-1
                elif Not(l) in literals:
                    if len(literals)==1:
                        formula = F
                        break
                    else:
                        literals.remove(Not(l))
                        if len(literals)==1:
                            formula = F
                            break
            else:
                if l in literals:
                    if len(literals)==1:
                        formula = F
                        break
                    else:
                        literals.remove(l.x)
                        if len(literals)==1:
                            formula = F
                            break
                elif Not(l) in literals:
                    clauses.remove(clause)
                    i, st_clauses = i-1, st_clauses-1
        elif isinstance(clause, Variable):
            if tf and clause==l:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
            elif clause == l:
                formula = F
                break
        elif isinstance(clause, Not):
            if tf and clause.x==l:
                formula = F
                break
            elif clause.x==l:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
    if st_clauses==0:
        return T
    else:
        return formula

                
                
