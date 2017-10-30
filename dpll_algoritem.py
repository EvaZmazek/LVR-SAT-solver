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
    
