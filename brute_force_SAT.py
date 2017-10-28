from boolean import *

def get_all_variables(spremenljivke,formula):
    if not isinstance(formula, Formula):
        return Error
    elif isinstance(formula, Variable):
        spremenljivke = spremenljivke + [formula.x]
    elif isinstance(formula, Not):
        spremenljivke = spremenljivke + [formula.x]
    elif isinstance(formula, Or):
        for clen in formula.terms:
            get_all_variables(spremenljivke, clen)
    elif isinstance(formula, And):
        for clen in formula.terms:
            get_all_variables(spremenljivke, clen)
    else:
        return "Kaj točno pa še ostane?"

def brut_force(spremenljivke):
    if len(spremenljivke)==0:
        print("nekaj")
        
