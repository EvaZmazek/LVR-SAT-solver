import copy
from boolean import*
import sys

F = Or()
T = And()

#možna izboljšava: p in Not(p) se skupaj pojavljata le v istam Oru
#oz. na en Or enkrat p in enkrat q

def get_all(formula, spremenljivke=None):
    #funkcija poišče vse spremenljivke formule, podane v CNF obliki
    if spremenljivke is None:
        spremenljivke = set()
    if isinstance(formula, Variable):
        spremenljivke.add(formula.x)
    elif isinstance(formula, Not):
        spremenljivke = spremenljivke.union(get_all(formula.x))
    elif isinstance(formula, And) or isinstance(formula, Or):
        for term in formula.terms:
            spremenljivke = spremenljivke.union(get_all(term))
    return spremenljivke

def get_all_V_NV(formula, spremenljivke=None, spremenljivke_Not=None):
    #funkcija poišče vse spremenljivke, ki nastopajo kot instanca razreda
    #Variable ter vse spremenljivke, ki nastopajo kot instanca razreda Not
    if spremenljivke is None:
        spremenljivke = set()
    if spremenljivke_Not is None:
        spremenljivke_Not = set()
    if isinstance(formula, Variable):
        spremenljivke.add(formula.x)
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
    
def simplify_unit_clauses(formula, koncni_valuation=None):
    #funkcija poenostavi formulo tako, da clause, ki so instance razreda
    #Variable, nastavi na vrednost True in clause, ki so razreda Not,
    #nastavi na False. Formulo poenostavi po spremenljivkah, ki so bile
    #določene.
    if koncni_valuation is None:
        koncni_valuation = dict()
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
                if len(literals) == 0:
                    return [F, koncni_valuation]
                if len(literals)==1:
                    if isinstance(literals[0], Variable):
                        valuation[literals[0].x]=True
                    elif isinstance(literals[0], Not):
                        valuation[literals[0].x.x]=False
    if len(valuation) == 0:
        return [formula, koncni_valuation]
    else:
        for var in valuation:
            koncni_valuation[var] = valuation[var]
            formula = simplify_by_literal(formula, var, valuation[var])
            if formula==T:
                return [T, koncni_valuation]
            elif formula == F:
                return [F, koncni_valuation]
        return simplify_unit_clauses(formula, koncni_valuation)
        

def simplify_pure_literals(formula, koncni_valuation=None):
    #funkcija, ki formulo formula poenostavi tako, da poišče spremenljivke, ki
    #nastopajo samo kot instance razreda Variable ali spremenljivke, ki
    #nastopajo samo kot instance razreda Not. Spremenljivke kot instance razreda
    #Variable nastavi na True ter poenostavi formulo glede na to spremenljivko.
    #Spremenljivke kot instance razreda Not pa nastavi na False ter poenostavi
    #formulo glede na to spremenljivko
    if koncni_valuation is None:
        koncni_valuation = dict()
    [pure_literals, pure_literals_Not]=find_pure_literals(formula)
    if len(pure_literals) == 0 and len(pure_literals_Not)==0:
        return [formula, koncni_valuation]
    else:
        for pure_lit in pure_literals:
            koncni_valuation[pure_lit] = True
            simplify_by_literal(formula, pure_lit, True)
        for pure_lit in pure_literals_Not:
            koncni_valuation[pure_lit] = False
            simplify_by_literal(formula, pure_lit, False)
        return simplify_pure_literals(formula, koncni_valuation)
    

def simplify_by_literal(formula, l, tf):
    #funkcija poenostavi formulo formula glede na spremenljivko l.
    clauses = formula.terms
    st_clauses = len(clauses)
    i = 0
    while i < st_clauses:
        clause = clauses[i]
        i = i+1
        if isinstance(clause, Variable):
            if (tf and clause==l) or clause==T:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
            elif (not tf and clause==l) or clause==F:
                return F
        if isinstance(clause, Not):
            if (tf and clause.x==l) or clause.x==T:
                return F
            elif (not tf and clause.x==l) or clause.x==F:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
        if isinstance(clause, Or):
            literals = clause.terms
            if len(literals)==0:
                return F
            if (l in literals and tf) or (Not(l) in literals and not tf) \
               or (T in literals):
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
            else:
                if l in literals and not tf:
                    literals.remove(l)
                if Not(l) in literals and tf:
                    literals.remove(Not(l))
                if F in literals:
                    literals.remove(F)
                if len(literals)==0:
                    return F
    if st_clauses == 0:
        return T
    else:
        return formula

def my_dpll(formula, koncni_valuation=None):
    #print("formula: " + str(formula))
    #funkcija po vrsti najprej poenostavi formulo glede na unit clause,
    #nato glede na pure literals. Za tem doda spremenljivke, ki so se izgubile
    #med poenostavljanjem formule. Nastavi jih na True.
    #če še formula nima vrednost T ali F, nastavi eno izmed
    #neznanih spremenljivk na True in preveri, če potem vrne rešitev.
    #če je rešitev unsatistiable, nastavi to spremenljivko na F in vrne rezultat
    unsatisfiable = "formula is unsatisfiable"
    if koncni_valuation is None:
        koncni_valuation = dict()
    spremenljivke_na_zacetku = get_all(formula)
    #print("POENOSTAVLJAM FORMULO GLEDE NA UNIT CLAUSE!!!!!!!!!")
    [formula, valuation_unit_clauses] = simplify_unit_clauses(formula)
    koncni_valuation.update(valuation_unit_clauses)
    #print("POENOSTAVLJAM FORMULO GLEDE NA PURE LITERALS!!!!!!!!!")
    [formula, valuation_pure_literals] = simplify_pure_literals(formula)
    #print(formula)
    koncni_valuation.update(valuation_pure_literals)
    #mogoče bi 3. del posebaj
    spremenljivke_zdaj = get_all(formula)
    #TA DEL NASTAVI VREDNOST SPREMENLJIVKAM, ZA KATERE
    #VREDNOSTI NEBI RABILI NASTAVITI - prišpara 5/1.2 % ČASA 
    for spremenljivka in spremenljivke_na_zacetku:
        if (spremenljivka not in koncni_valuation) and \
           (spremenljivka not in spremenljivke_zdaj):
            koncni_valuation[spremenljivka] = True
    #če je velikost spremenljivk zdaj enaka 0, vrni rezultat
    if formula == T:
        return koncni_valuation
    elif formula == F:
        return unsatisfiable
    elif len(spremenljivke_zdaj) == 0:
        return koncni_valuation
    else:
        formula_shrani = copy.deepcopy(formula)
        valuation_shrani = copy.deepcopy(koncni_valuation)
        spr = spremenljivke_zdaj.pop()
        koncni_valuation[spr] = True
        formula = simplify_by_literal(formula, spr, True)
        globina = my_dpll(formula, koncni_valuation)
        if globina != unsatisfiable:
            return globina
        else:
            valuation_shrani[spr] = False
            formula_shrani = simplify_by_literal(formula_shrani, spr, False)
            return my_dpll(formula_shrani, valuation_shrani)
