from boolean import *
from dpll_algoritem import *

f = And("p", Or(Not("p"), "q"), Or(Not("p"), Not("q"), "r"))
print(simplify_unit_clauses(f))

f = And("p", Or("p", "r"), Or(Not("r"), Not("q"),"q"))
print(simplify_pure_literals(f))

f = And("p", Or("p", "r"), Or(Not("r"), "q"))
print(simplify_pure_literals(f))

f = And(Or("p", "q","r"), Or("p", Not("q")), Or(Not("p"), "q"))
print(simplify_pure_literals(f))
