from itertools import chain, combinations
import math
import ExtenRelat

offsetVertical = 2
offsetHorizontal = 3

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def createBoolean(groundSet):
    n = len(groundSet)
    places = []
    links = []
    PS = powerset(groundSet)
    PS = list(PS)
    for size in range(n+1):
        #trouver les ensembles
        index = 0
        for k in range(size):
            index += int(math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))
        #récupérer les ensembles de taille size
        nbEns = int(math.factorial(n)/(math.factorial(size)*math.factorial(n-size)))
        for indEns in range(index,index+nbEns):
            #leur attribuer la bonne coordonnée horizontale
            x = ((indEns-index)*offsetHorizontal)-((nbEns-(nbEns%2))*offsetHorizontal)/2
            y = size*offsetVertical
            places.append([list(PS[indEns]),x,y])

        if size < n:
            index2 = index + nbEns
            nbEns2 = int(math.factorial(n)/(math.factorial(size+1)*math.factorial(n-size-1)))
            for indEns in range(index,index+nbEns):
                for indEns2 in range(index+nbEns,index+nbEns+nbEns2):
                    if set(PS[indEns]).issubset(set(PS[indEns2])):
                        links.append([indEns,indEns2])

    return places,links


def plotExtensionRelation(extRel):
    #retrouver le groundset
    groundSet = []
    for S in extRel[1]:
        for s in S:
            groundSet.append(s)

    n = len(groundSet)
    places = []
    links = []
    PS = powerset(groundSet)
    PS = list(PS)
    for size in range(n+1):
        #trouver les ensembles
        index = 0
        for k in range(size):
            index += int(math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))
        #récupérer les ensembles de taille size
        nbEns = int(math.factorial(n)/(math.factorial(size)*math.factorial(n-size)))
        for indEns in range(index,index+nbEns):
            #leur attribuer la bonne coordonnée horizontale
            x = ((indEns-index)*offsetHorizontal)-((nbEns-(nbEns%2))*offsetHorizontal)/2
            y = size*offsetVertical
            places.append([list(PS[indEns]),x,y])

        #ajouter les arêtes
        if size < n:
            index2 = index + nbEns
            nbEns2 = int(math.factorial(n)/(math.factorial(size+1)*math.factorial(n-size-1)))
            for indEns in range(index,index+nbEns):
                for indEns2 in range(index+nbEns,index+nbEns+nbEns2):
                    add = False
                    for X in extRel[0][PS[indEns]]:
                        if set(PS[indEns]).issubset(set(PS[indEns2])) and set(PS[indEns2]).issubset(set(X)):
                            add = True
                            break
                    if add:
                        links.append([indEns,indEns2])

    return places,links


def plotExtensionRelationNB(extRel):
    #retrouver le groundset
    groundSet = []
    for S in extRel[1]:
        for s in S:
            groundSet.append(s)

    n = len(groundSet)
    places = []
    links = []
    PS = powerset(groundSet)
    PS = list(PS)
    Presents = []
    for size in range(n+1):
        #trouver les ensembles
        index = 0
        for k in range(size):
            index += int(math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))
        #récupérer les ensembles de taille size
        nbEns = int(math.factorial(n)/(math.factorial(size)*math.factorial(n-size)))
        for indEns in range(index,index+nbEns):
            #Si l'ensemble est strictement entre une prémisse et une conclusion
            add = True
            for indTest in range(index):
                if set(PS[indTest]).issubset(set(PS[indEns])):
                    for S in extRel[0][PS[indTest]]:
                        if set(PS[indEns]).issubset(set(S)) and not set(S).issubset(set(PS[indEns])):
                            add = False
                            break
                if not add:
                    break
            if add:
            #leur attribuer la bonne coordonnée horizontale
                Presents.append(indEns)
                x = ((indEns-index)*offsetHorizontal)-((nbEns-(nbEns%2))*offsetHorizontal)/2
                y = size*offsetVertical
                places.append([list(PS[indEns]),x,y])

    print("Presents",Presents)
    for i in range(len(Presents)-1):
        #ajouter les arêtes
            print("Je teste",list(PS[Presents[i]]))
            conclusions = []
            for j in range(i+1,len(Presents)):
                print("Est-ce que",list(PS[Presents[j]]),"est dans",extRel[0][PS[Presents[i]]])
                if list(PS[Presents[j]]) in extRel[0][PS[Presents[i]]]:
                    print("oui")
                    links.append([i,j])
                    print("J'ajoute",PS[Presents[i]],"=>",PS[Presents[j]])
                else:
                    print("non")

    return places,links



def format(liste,names):
    if len(liste) == 0:
        return "$\\emptyset$"
    S = "\\{"
    for l in range(len(liste)-1):
        S += str(names[liste[l]])+","
    S += str(names[liste[len(liste)-1]])+"\\}"
    return S

def drawLattice(fileName,places,links,names):
    f = open(fileName,"w")
    f.write("\\begin{tikzpicture}[-]\n")
    f.write("\n")
    for p in range(len(places)):
        #\node (bot) at (0,0) {$\emptyset$};
        f.write("\\node ("+str(p)+") at ("+str(places[p][1])+","+str(places[p][2])+") {"+format(places[p][0],names)+"};\n")
    f.write("\n")
    f.write("\\path[]\n")
    for l in links:
        #(bot) edge[->] (a1)
        f.write("("+str(l[0])+") edge[->] ("+str(l[1])+")\n")
    f.write(";\n")
    f.write("\n")
    f.write("\\end{tikzpicture}")
    f.close()
