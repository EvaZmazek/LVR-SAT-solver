from boolean import*

def get_all(formula, spremenljivke=set()):
    #funkcija poišče vse spremenljivke formule, podane v CNF obliki
    if isinstance(formula, Variable):
        spremenljivke = spremenljivke.union(formula.x)
    elif isinstance(formula, Not):
        spremenljivke = spremenljivke.union(get_all(formula.x))
    elif isinstance(formula, And) or isinstance(formula, Or):
        for term in formula.terms:
            spremenljivke = spremenljivke.union(get_all(term))
    return spremenljivke

def get_all_V_NV(formula, spremenljivke=set(), spremenljivke_Not=set()):
    #funkcija poišče vse spremenljivke, ki nastopajo kot instanca razreda
    #Variable ter vse spremenljivke, ki nastopajo kot instanca razreda Not
    if isinstance(formula, Variable):
        spremenljivke = spremenljivke.union(formula.x)
    elif isinstance(formula, Not):
        spremenljivke_Not = spremenljivke_Not.union(get_all_V_NV(formula.x)[0])
    elif isinstance(formula, And) or isinstance(formula, Or):
        for term in formula.terms:
            [spremenljivke_nove, spremenljivke_Not_nove] = get_all_V_NV(term)
            spremenljivke = spremenljivke.union(spremenljivke_nove)
            spremenljivke_Not = spremenljivke_Not.union(spremenljivke_Not_nove)
    return [spremenljivke, spremenljivke_Not]

def find_pure_literals(formula):
    #funkcija poišče vse spremenljivke, ki nastopajo samo kot instance razreda
    #Variable in vse spremenljivke, ki nastopajo samo kot instance razreda Not
    variables, variables_not = get_all_V_NV(formula)
    pure_literals = []
    pure_literals_not = []
    for var in variables.union(variables_not):
        if (var in variables and var not in variables_not):
            pure_literals.append(var)
        elif (var in variables_not and var not in variables):
            pure_literals_not.append(var)
    return [pure_literals, pure_literals_not]
    
def simplify_unit_clauses(formula, koncni_valuation=dict()):
    print("poenostavljam unit clauses:" + str(formula) + "!!!!!:")
    print("koncni_valuation:" + str(koncni_valuation))
    valuation = dict()
    clauses = formula.terms
    st_clauses = len(clauses)
    i=0
    while i < st_clauses:
        clause = clauses[i]
        i = i+1
        if isinstance(clause, Variable):
            valuation[clause.x] = True
        elif isinstance(clause, Not):
            valuation[clause.x.x] = False
        elif isinstance(clause, Or):
            literals = clause.terms
            if T in literals:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
            else:
                if F in literals:
                    literals.remove(F)
                if len(literals)==1:
                    if isinstance(literals[0], Variable):
                        valuation[literals[0].x]=True
                    elif isinstance(literals[0], Not):
                        valuation[literals[0].x.x]=False
    print("plegleda vse clause in doda stvari v:" + str(valuation))
    if len(valuation) == 0:
        print([formula, koncni_valuation])
        return [formula, koncni_valuation]
    else:
        for var in valuation:
            koncni_valuation[var] = valuation[var]
            formula = simplify_by_literal(formula, var, valuation[var])
            if formula==T:
                print([T, koncni_valuation])
                return [T, koncni_valuation]
            elif formula == F:
                print([F, koncni_valuation])
                return [F, koncni_valuation]
        return simplify_unit_clauses(formula, koncni_valuation)
        

def simplify_pure_literals(formula):
    #funkcija, ki formulo formula poenostavi tako, da poišče spremenljivke, ki
    #nastopajo samo kot instance razreda Variable ali spremenljivke, ki
    #nastopajo samo kot instance razreda Not. Spremenljivke kot instance razreda
    #Variable nastavi na True ter poenostavi formulo glede na to spremenljivko.
    #Spremenljivke kot instance razreda Not pa nastavi na False ter poenostavi
    #formulo glede na to spremenljivko
    pass

def simplify_by_literal(formula, l, tf):
    #funkcija poenostavi formulo formula glede na spremenljivko l.
    print("poenostavljam po spremenljivki " + str(l) + ":" + str(formula) + "!!!!!!:")
    clauses = formula.terms
    st_clauses = len(clauses)
    i = 0
    while i < st_clauses:
        clause = clauses[i]
        i = i+1
        if isinstance(clause, Variable):
            print("Variable:" + str(clause))
            if (tf and clause==l) or clause==T:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
            elif (not tf and clause==l) or clause==F:
                return F
        if isinstance(clause, Not):
            print("Not:" + str(clause))
            if (tf and clause.x==l) or clause.x==T:
                return F
            elif (not tf and clause.x==l) or clause.x==F:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
        if isinstance(clause, Or):
            print("Or:" + str(clause))
            literals = clause.terms
            if len(literals)==0:
                print("literals je prazen")
                return F
            if (l in literals and tf) or (Not(l) in literals and not tf) \
               or (T in literals):
                print("v literals so že l(True) ali Not(l) (False) ali T")
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
                print(formula)
            else:
                if l in literals and not tf:
                    print("v literals l in False")
                    literals.remove(l)
                if Not(l) in literals and tf:
                    print("v literals Not(l) in True")
                    literals.remove(Not(l))
                if F in literals:
                    print("v literals F")
                    literals.remove(F)
                if len(literals)==0:
                    return F
                print(formula)
    if st_clauses == 0:
        return T
    else:
        return formula
