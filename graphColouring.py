from boolean import*
#tako ni treba pisati boolean._
#z import boolean bi bilo treba

#       0     1      2       3       4
#G = [[1,2],[0,3],[0,3,4],[1,2,4], [2,3]]

def graphColouring2SAT(G, k):
    conj = []
    for i in range(len(G)):
        conj.append(Or(*((i,j) for j in range(k))))
        #vsako vozlišče je neke barve
        #(i,j) je spremenljivka ker še ni instanca razreda Formula
        #--> makeFormula jo naredi v spremenljivko
        for j in range(k):
            for jj in range(j+1,k):
                conj.append(Or(Not((i,j)), Not((i,jj))))
        for h in G[i]:
            for j in range(k):
                conj.append(Or(Not((i,j)), Not((i,jj))))
    return And(*conj)

#####################   UPORABA DATOTEKE    #########################
#import graphColouring
#G = [[1,2],[0,3],[0,3,4],[1,2,4], [2,3]]
#c2 = graphColouring.graphColouring2SAT(G,2)
#print(c2)
#c3 = graphColouring.graphColouring2SAT(G,3)
#print(c3)
#col = {0: 0, 1:1, 2:1, 3:0, 4:2}
#d = {}
#for i in range(5):
#	for j in range(3):
#		d[(i,j)] = (i,j) in col.items()

def SAT2graphColouring(sol):
    d = {i:j for (i,j), v in sol.items() if v}
    out = [None]*len(d)
    for i, j in d.items():
        out[i] = j
    return out
