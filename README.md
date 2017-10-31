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
 * Nastavi končni_valuation na prazen slovar, če ta ni že podan (na začetku None, da ne uporabi končni_valuation od katerega primera od prej).
 ```python3
    if koncni_valuation is None:
        koncni_valuation = dict()
   ```
 * v seznam spremenljivke_na_zacetku da vse premenljivke iz formule formula
 * poenostavi formulo glede na unit clause. Znotaj poenostavljanja določi vrednosti nekaterih spremenljivk. Te shrani v slovar
 valuation_unit_clauses. Vrednosti spremenljivk iz slovarja valuation_unit_clauses doda slovarju koncni_valuation:
 ```python3
 koncni_valuation.update(valuation_unit_clauses)
 ```
 * poenostavi formulo glede na pure literals. Znotaj poenostavljanja določi vrednosti nekaterih spremenljivk. Te shrani v slovar valuation_pure_literals. Vrednosti spremenljivk iz slovarja valuation_pure_literals doda slovarju koncni_valuation:
  ```python3
 koncni_valuation.update(valuation_pure_literals)
 ```
 * v seznam spremeljivke_zdaj shrani spremenljivke, ki še niso bile določene do tega koraka.
 * Spremenljivke, ki so bile na začetku v formuli, po poenostavljanju pa jih ni več ter jim med poenostavljanjem nismo določili vrednosti, nastavimo na True:
 ```python3
     for spremenljivka in spremenljivke_na_zacetku:
        if (spremenljivka not in koncni_valuation) and \
           (spremenljivka not in spremenljivke_zdaj):
            koncni_valuation[spremenljivka] = True
 ```
 * preverimo, ali smo formulo poenostavili do vrednosti T. Če smo, je naša formula satisfiable z valuation koncni_valuation.
 * preverimo, ali smo formulo poenostavili do vrednosti F. Če smo, naša formula ni satisfiable.
 * Če še ne vemo, ali je formula satisfiable ali ni satisfiable, pomeni, da moramo določiti vrednost ene izmed spremenljivk.
 Najprej naredimo kopijo naše formule ter kopijo našega slovarja valuation.
 ```python3
 formula_shrani = copy.deepcopy(formula)
 valuation_shrani = copy.deepcopy(koncni_valuation)
```
Izberemo prvo spremenljivko, ki še nima določene vrednosti.
Vrednost te spremenljivke nastavimo na True.
ponovno poskusimo priti do rešitve s rekurzivnim klicom na obstoječi formuli in obstoječem seznamu. Če nam uspe, vrnemo to rešitev, sicer uporabimo kopiji formule in seznama pred "ugibanjem" ter na teh kopijah poskusimo priti do rešitve. Ker v tem primeru za vrednost izbrane spremenljivke True, formula ni satifiable, je edina možnost, da je satisfiable le tista, pri kateri je vrednost izbrane spremenljivke enaka False. Če tudi v tem primeru formula ni satisfiable, potem ni satisfiable v nobenem primeru. Zato lahko vrnemo kar rešitev rekurzivnega klica my_dpll(formula_shrani, valuation_shrani).
