from boolean import *

#predpostavljamo, da je formula podana v CNF obliki

def get_all(formula, spremenljivke=set()):
    if isinstance(formula, Variable):
        spremenljivke = spremenljivke.union(formula.x)
    elif isinstance(formula, Not):
        spremenljivke = spremenljivke.union(get_all(formula.x))
    elif isinstance(formula, And) or isinstance(formula, Or):
        for term in formula.terms:
            spremenljivke = spremenljivke.union(get_all(term))
    return spremenljivke

def get_all_CNF(formula, spremenljivke=set(), spremenljivke_Not=set()):
    if isinstance(formula, Variable):
        spremenljivke = spremenljivke.union(formula.x)
    elif isinstance(formula, Not):
        spremenljivke_Not = spremenljivke_Not.union(get_all_CNF(formula.x)[0])
    elif isinstance(formula, And) or isinstance(formula, Or):
        for term in formula.terms:
            [spremenljivke_nove, spremenljivke_Not_nove] = get_all_CNF(term)
            spremenljivke = spremenljivke.union(spremenljivke_nove)
            spremenljivke_Not = spremenljivke_Not.union(spremenljivke_Not_nove)
    return [spremenljivke, spremenljivke_Not]

def my_dpll(formula, valuation=dict()):
    vse_spremenljivke = get_all(formula)
    st_vseh_spremenljivk = len(vse_spremenljivke)
    zacetna = And(*formula.terms) #to se verjetno da kako izboljšati
    vrednost = simplify_unit_clause(formula, valuation)
    if not vrednost:
        return False
    spremenljivke, spremenljivke_Not = get_all_CNF(formula)
    pure_literal = []
    prva_dolzina = len(valuation)
    ostale_spremenljivke = spremenljivke.union(spremenljivke_Not)
    for spre in ostale_spremenljivke:
        if (spre in spremenljivke and spre not in spremenljivke_Not) \
           or (spre not in spremenljivke and spre in spremenljivke_Not):
            pure_literal.append(spre)
    #ne rabimo pazit na že vnešene vrednosti, ker v novi formuli teh spremenljivk ni več
    #(so že poenostavljene iz formule)
    for plit in pure_literal:
        #TODO nevem, če je treba iti čez vse. Lahko se katera že prej izbriše!!!!!!
        if plit in spremenljivke:
            valuation[plit] = True
            print("poenostavljam zaradi pure variable")
            vrednost = simplify_by_literal(formula, plit, True)
            if vrednost == F:
                return False
            if vrednost == T:
                for spremenljivka in vse_spremenljivke:
                    if spremenljivka not in valuation:
                        valuation[spremenljivka] = True
                return valuation
        else:
            valuation[plit] = False
            print("poenostavljam zaradi pure variable")
            vrednost = simplify_by_literal(formula, plit, False)
            if vrednost == F:
                return False
            if vrednost == T:
                for spremenljivka in vse_spremenljivke:
                    if spremenljivka not in valuation:
                        valuation[spremenljivka] = True
                return valuation
    nedolocene_spremenljivke = get_all(formula)
    if len(nedolocene_spremenljivke)==0:
        if len(valuation)==st_vseh_spremenljivk and zacetna.evaluate(valuation):
            return valuation
        for spremenljivka in vse_spremenljivke:
            if spremenljivka not in valuation:
                valuation[spremenljivka] = True
            if zacetna.evaluate(valuation):
                return valuation
            else:
                return False
    else:
        print("grem preizkušat:")
        doloci_l = nedolocene_spremenljivke.pop()
        print(formula)
        my_dpll(formula, valuation)
        return valuation

def simplify_unit_clause(formula, valuation=dict()):
    print("iščem unit clause")
    clauses = formula.terms
    print(formula)
    st_clauses = len(clauses)
    i = 0
    while i < st_clauses:
        clause = clauses[i]
        i = i+1
        if isinstance(clause, Or):
            literals = clause.terms
            if len(literals)==1:
                clauses.remove(clause)
                clause = literals[0]
                if isinstance(clause, Variable):
                    valuation[clause.x]=True
                    print("izbrišem en unit clause")
                    vrednost = simplify_by_literal(formula, clause.x, True)
                    if not vrednost:
                        return False
                elif isinstance(clause, Not):
                    valuation[clause.x.x]=False
                    print("izbrišem en unit clause")
                    vrednost = simplify_by_literal(formula, clause.x.x, False)
                    if vrednost==F:
                        return False
                simplify_unit_clause(formula, valuation)
                return valuation
        elif isinstance(clause, Variable):
            valuation[clause.x]=True
            clauses.remove(clause)
            print("izbrišem en unit clause")
            vrednost = simplify_by_literal(formula, clause.x, True)
            if vrednost==F:
                return False
            simplify_unit_clause(formula, valuation)
            return valuation
        elif isinstance(clause, Not):
            valuation[clause.x.x]=False
            clauses.remove(clause)
            print("izbrišem en unit clause")
            vrednost = simplify_by_literal(formula, clause.x.x, False)
            if vrednost==F:
                return False
            simplify_unit_clause(formula, valuation)
            return valuation

def simplify_pore_literal(formula, valuation):
    #mogoče pojdi čez seznam vseh spremenljivk in označi, če je spremenljivka (nastavi na true),
    #če je negacija (nastavi na false) in preglejuj če se kdaj seka --> odstrani iz seznama pure
    #pure literal. Na začetku nastavi na none
    pass

def simplify_by_literal(formula, l, tf):
    print(formula)
    print("poenostavljam po spremenljivki " + str(l))
    clauses = formula.terms
    st_clauses = len(clauses)
    i = 0
    while i < st_clauses:
        clause = clauses[i]
        i = i+1
        if isinstance(clause, Or):
            literals = clause.terms
            if len(literals)==0:
                return F
            elif tf:
                if l in literals:
                    clauses.remove(clause)
                    i, st_clauses = i-1, st_clauses-1
                if Not(l) in literals:
                    if len(literals)==1:
                        return F
                    else:
                        literals.remove(Not(l))
                        if len(literals)==1:
                            return F
            else:
                if l in literals:
                    if len(literals)==1:
                        return F
                    else:
                        literals.remove(l)
                        if len(literals)==1:
                            return F
                if Not(l) in literals:
                    clauses.remove(clause)
                    i, st_clauses = i-1, st_clauses-1
        elif isinstance(clause, Variable):
            if tf and clause==l:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
            elif clause == l:
                return F
        elif isinstance(clause, Not):
            if tf and clause.x==l:
                return F
            elif clause.x==l:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
    if st_clauses==0:
        return T
    else:
        return formula

                
                
