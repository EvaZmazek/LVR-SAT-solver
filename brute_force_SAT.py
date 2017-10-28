from boolean import *

def get_all(formula, spremenljivke=set()):
    if isinstance(formula, Variable):
        spremenljivke = spremenljivke.union(formula.x)
    elif isinstance(formula, Not):
        spremenljivke = spremenljivke.union(get_all(formula.x))
    elif isinstance(formula, And) or isinstance(formula, Or):
        for term in formula.terms:
            spremenljivke = spremenljivke.union(get_all(term))
    else:
        print("ni še obdelan if")
    return spremenljivke

def list_spremenljivk(formula):
    spremenljivke = list(get_all(formula))
    return spremenljivke

def brute_force(formula):
    spremenljivke = list_spremenljivk(formula)
    def search(spremenljivke, v, formula):
        if len(spremenljivke)==0:
            if formula.evaluate(v):
                print(v)
                return True
            else:
                return False
        else:
            spremenljivka = spremenljivke[0]
            spremenljivke = spremenljivke[1:]
            v[spremenljivka] = True
            if search(spremenljivke, v, formula):
                return True
            v[spremenljivka] = False
            if search(spremenljivke, v, formula):
                return True
            return False
    if search(spremenljivke, dict(), formula):
        return "formula je satisfiable"
    else:
        return "formula ni satisfiable"
