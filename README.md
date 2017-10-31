### SAT-solver
An (incomplete) SAT solver

## IMPLEMENTING DPLL ALGORITEM

Pomožnje fonckije, uporabljene za dpll algoritem:
# get_all(formula, spremenljivke = None)

# get_all_V_NV(formula, spremenljivke=None, spremenljivke_Not=None)

# find_pure_literals(formula)

# simplify_unit_clauses(formula, koncni_valuation=None)

# simplify_pure_literals(formula, koncni_valuation=None)

# simplify_by_literal(formula, l, tf)

Glavni del programa:
# my_dpll(formula, koncni_valuation=None)
 Ta algoritem po vrsti naredi:
 * ´´´
    if koncni_valuation is None:
        koncni_valuation = dict()
   ´´´
 *
 *
 *
 *
 
