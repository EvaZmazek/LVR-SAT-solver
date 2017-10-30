import copy
from boolean import *
from dpll_algoritem import *

testni_primeri = []
pravilnosti_testnih_primerov = []

f = And("p", Or(Not("p"), "q"), Or(Not("p"), Not("q"), "r"))
testni_primeri.append(f)
#print(simplify_unit_clauses(f))

f = And("p", Or("p", "r"), Or(Not("r"), Not("q"),"q"))
testni_primeri.append(f)
#print(simplify_pure_literals(f))

f = And("p", Or("p", "r"), Or(Not("r"), "q"))
testni_primeri.append(f)
#print(simplify_pure_literals(f))

f = And(Or("p", "q","r", "m"), Or("p", Not("q")), Or(Not("p"), "q"), "r", Or("l", "p"), Or(Not("p"), Not("m")))
testni_primeri.append(f)
#print(simplify_pure_literals(f))

#print(my_dpll(f))

f = And()
testni_primeri.append(f)
#print(my_dpll(f))

f = And("P")
testni_primeri.append(f)
#print(my_dpll(f))

f = And(Not("p"))
testni_primeri.append(f)
#print(my_dpll(f))

f = And(Or("p", "q"))
testni_primeri.append(f)
#print(my_dpll(f))

f = And(Or("p", Not("q")))
testni_primeri.append(f)
#print(my_dpll(f))

f = And("p", Not("p"))
testni_primeri.append(f)

unsatisfiable = "formula is unsatisfiable"

for test in testni_primeri:
    testtest = copy.deepcopy(test)
    valuation = my_dpll(test)
    #print(valuation)
    #print(ff.evaluate(valuation))
    if valuation == unsatisfiable:
        pravilnosti_testnih_primerov.append(None)
    else:
        pravilnosti_testnih_primerov.append(testtest.evaluate(valuation))
print(pravilnosti_testnih_primerov)
