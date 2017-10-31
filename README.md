# SAT-solver
CLAUSE = STAVEK
LITERAL = LITERAL

An (incomplete) SAT solver

## IMPLEMENTING DPLL ALGORITEM

Pomožnje fonckije, uporabljene za dpll algoritem:
### get_all(formula, spremenljivke = None)
Ta funkcija vrne množico vseh spremenljivk v obliki konstruktorja (konstruktor od Not("p") je "p").

### get_all_V_NV(formula, spremenljivke=None, spremenljivke_Not=None)
Funkcija get_all_V_NV sprejme formulo ter vrne množico spremenljivk, ki nastopajo kot instance razreda Variable. Ta množica je poimenovana spremenljivke. Hkrati vrne tudi množico spremenljivk, ki nastopajo kot instance razreda Not. Ta množica je poimenovana spremenljivke_Not. Tako kot pri funkciji get_all, so tudi tu spremenljivke v množicah podane v obliki konstruktorja.

### find_pure_literals(formula)
Funkcija find_pure_literals sprejme formulo ter vrne seznam spremenljivk, ki nastopajo le kot instance razreda Variable. Ta seznam je poimenovan pure_literals. Hkrati vrne tudi seznam spremenljivk, ki nastopajo le kot instance razreda Not. Ta seznam je poimenovan pure_literals_not. Podobno kot pri funkcijah get_all in get_all_V_NV so spremenljivke v seznamih podane v obliki konstruktorja.

### simplify_unit_clauses(formula, koncni_valuation=None)
Zaradi avtomatskega shranjevanja koncni_valuation nastavimo na None, če ni podan in ga kasneje spremenimo v prazen clovar, če je None:
```python3
    if koncni_valuation is None:
        koncni_valuation = dict()
```
Znotraj te funkcije bomo nastavili nekatere vrednosti spremenljivk, ki si jih bomo shranjevali v slovar valuation. Ločen slovar, da na koncu vemo, katere smo dodali.
Pripravimo si seznam stavkov (clauses) ter pogledamo njegovo dolžino. Kazalec i nastavimo na 0 (kazalec za while funkcijo).
```python3
    clauses = formula.terms
    st_clauses = len(clauses)
    i=0
```
Ker bomo med while funkcijo brisali nekatere stavke, se čez njih sprehodimo z while zanko in ne for zanko. 

Pogledamo v katerem stavku se nahajamo ter pripravimo kazalec za naslednji stavek:
```python3
        clause = clauses[i]
        i = i+1
```
V primeru, ko je stavek kar enak spremenljivki, tej spremenljivki nastavimo vrednost na True.
```python3
        if isinstance(clause, Variable):
            valuation[clause.x] = True
```
V primeru, ko je stavek enak instanci razreda Not, spremenljikvki v razredu Not nastavimo vrednost na False.
```python3
        elif isinstance(clause, Not):
            valuation[clause.x.x] = False
```

V primeru, ko je stavek enak instanci razreda Or, najprej v tem razredu preverimo, če je kateri od literalov enak T (DODATEK (ni v osnovni verziji dpll algoritma)). Če je, je celotni stavek enak True in zato lahko ta stavek iz formule izbrišemo. Pri tem moramo paziti na kazalec i ter novo število stavkov st_clauses.
```python3
            if T in literals:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
```
Če je kateri od literalov enak F, ga lahko odstranimo (DODATEK (ni v osnovni verziji dpll algoritma)).
```python3
            else:
                if F in literals:
                    literals.remove(F)
```
Če smo tako izbrisali vse literale, je celotna formula enaka F:
```python3
                if len(literals) == 0:
                    return [F, koncni_valuation]
```

Na tem koraku pa zdaj preverimo, ali je dolžina literals enaka 1, torej ali to vbistvu predstavlja instanco razreda Variable ali pa instanco razreda Not:
```python3
                if len(literals)==1:
                    if isinstance(literals[0], Variable):
                        valuation[literals[0].x]=True
                    elif isinstance(literals[0], Not):
                        valuation[literals[0].x.x]=False
```

Če na enem koraku ne nastavimo vrednosti nobeni novi spremenljivki, pomeni da formule ne moremo več bolj poenostaviti glede na unit clause, zato vrnemo poenostavljeno formulo skupaj s slovarjem nastavljenih vrednost:
```python3
    if len(valuation) == 0:
        return [formula, koncni_valuation]
```

Če smo v prejšnjih korakih nastavili nove vrednosti, zdaj poenostavimo formulo glede na te vrednosti ter ponovimo postopek z novo poenostavljeno formulo (rekurzivni klic):
```python3
    else:
        for var in valuation:
            koncni_valuation[var] = valuation[var]
            formula = simplify_by_literal(formula, var, valuation[var])
            if formula==T:
                return [T, koncni_valuation]
            elif formula == F:
                return [F, koncni_valuation]
        return simplify_unit_clauses(formula, koncni_valuation)
```

### simplify_pure_literals(formula, koncni_valuation=None)
Zaradi avtomatskega shranjevanja koncni_valuation nastavimo na None, če ni podan in ga kasneje spremenimo v prazen clovar, če je None:
```python3
    if koncni_valuation is None:
        koncni_valuation = dict()
```

Najprej pogledamo katere so naše "pure literals":
```python3
[pure_literals, pure_literals_Not]=find_pure_literals(formula)
```

Če jih ni, vrnemo formulo ter slovar na novo nastavljenih vrednosti:
```python3
    if len(pure_literals) == 0 and len(pure_literals_Not)==0:
        return [formula, koncni_valuation]
```

Sicer za vsako "pure literal" pogledamo ali je "pure literal" tipa Variable (v tem primeru nastavimo vrednost spremenljivke na True ter poenostavimo formulo glede na to spremenljivko), ali je "pure literal" tipa Not (v tem primeru nastavimo vrednost spremenljivke na False ter poenostavimo formulo glede na to spremenljivko). Na koncu se funkcija rekurzivno pokliče (v primeru, da smo kaj spremenili):
```python3
    else:
        for pure_lit in pure_literals:
            koncni_valuation[pure_lit] = True
            simplify_by_literal(formula, pure_lit, True)
        for pure_lit in pure_literals_Not:
            koncni_valuation[pure_lit] = False
            simplify_by_literal(formula, pure_lit, True)
        return simplify_pure_literals(formula, koncni_valuation)
```

### simplify_by_literal(formula, l, tf)
Funkcija simplify_by_literal(formula, l , tf) prejme formulo, spremenljivko l ter vrednost te spremenljivke tf (True ali False). Podobno kot v funkciji simplify_unit_clauses razdeli formulo na stavke ter si pripravi kazalec i ter stevilo stavkov st_clauses za while zanko:

```python3
    clauses = formula.terms
    st_clauses = len(clauses)
    i = 0
```

Znotral while zanke pogledamo v katerem stavku se nahajamo ter pripravimo kazalec za naslednji stavek:
```python3
        clause = clauses[i]
        i = i+1
```

Ločimo tri primere za stavek clause:
1. stavek je tipa Variable:
Če je spremenljivka (clause) enaka spremenljivki po kateri poenostavljamo (l) ter ima spremenljivka l vrednost True ali če je spremenljivka enaka T, izbrišemo stavek ter pri tem pazimo na vrednosti i ter st_clauses. Če je spremenljivka clause enaka spremenljivki l ter ima spremenljivka l vrednost False ali če je spremenljivka enaka F, potem je celotna formula enaka F:
```python3
        if isinstance(clause, Variable):
            if (tf and clause==l) or clause==T:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
            elif (not tf and clause==l) or clause==F:
                return F
```


2. stavek je tipa Not:
Če je spremenljivka clause.x (clause=Not(clause.x)) enaka spremenljivki l ter ima spremenljivka l vrednost True ali je spremenljivka clause.c enaka T, je celotna formula enaka F. Če je spremenljivka clause.x enaka spremenljivki l ter ima spremenljivka l vrednost F ali če je spremenljivka clause.x enaka F, izbrišemo stavek ter pri tem pazimo na vrednosti i ter st_clauses:
```python3
        if isinstance(clause, Not):
            if (tf and clause.x==l) or clause.x==T:
                return F
            elif (not tf and clause.x==l) or clause.x==F:
                clauses.remove(clause)
                i, st_clauses = i-1, st_clauses-1
```

3. stavek je tipa Or:
Argumenti instance razreda Or shranimo v slovar literals. Če je ta slovar prazen, je vrednost celotne formule enaka F. Če je spremenljivka l v tem slovarju in je njena vrednost enaka True, je celoten stavek enak T. Prav tako je celoten stavek enak T, če je med literals Not(l) in je vrednost l enaka False. Če je T element seznama literals, je formula enaka T ne glede na ostale elemente seznama literals. V teh primerih lahko stavek izbrišemo ter pri tem pazimo na vrednosti i ter st_clauses.
Če se v seznamu literals nahaja spremenljivka l in je ta spremenljivka nastavljena na False ali pa če se je v seznamu literals Not(l) in je vrednost spremenljivke l enaka True, lahko te člene izbrišemo iz seznama literals (želimo namreč vrednosti, ki so enake T). Prav tako lahko izbrišemo vse parametre, ki so enaki F. Na koncu preverimo, če nam je v seznamu literals še ostal kakšen element. Če nam ni, je naš stavek enak Or(), kar je enako F. Formula v tem primeru vrne F.
```python3
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
```

Na tem koraku (zunaj while zanke) preverimo tudi, če je število stavkov st_clauses enako nič. Če je, je formula enaka And()=T.
Vrnemo našo novo formulo:
```python3
    if st_clauses == 0:
        return T
    else:
        return formula
```

Glavni del programa:
## my_dpll(formula, koncni_valuation=None)
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

##POGANJANJE DATOTEK V FORMATU DINAMIC FORMAT

#dinamic format:

*vrstice, ki se začnejo s črko c, so komentarji
*vrstica, ki se začne s črko p, poda po vrsti obliko formule (v našem primeru cnf oblika), število spremenljivk v ter število stavkov c.
*vsaka naslednja vrstica predstavlja stavek. Literali so ločeni s presledki. Literal tipa Variable je podan kot pozitivno število, literal tipa Not pa kot negativno število (Not("1")="-1"). Na koncu vsakega stavka je število 0.

 ```txt
c komentar1
c komentar2
p cnf v c
l1 l2 0
l3 l4 l5 0
l6 l7 l8 l9 0
```

Primer dinamic formata:
 ```txt
c example9
c example for And(Or(Not("p"), Not("q")))
p cnf 2 1
-1 -2 0
```

Datoteko s primerom poženemo s pomočjo funkcije dpll_run:
```
Evas-MBP:LVR-SAT-solver evazmazek$ python3 dpll_run.py 'testing_files/example9.txt' 'outputfilename.txt'
```
