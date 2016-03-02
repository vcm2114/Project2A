import pandas as pd
import numpy as np
from xlrd101 import import_xls

# Définition d'une classe concept formel

class FormalConcept:
    """un concept formel est défini par 
    - un ensemble d'objets
    - un ensemble d'attributs"""
    
    def __init__(self,obj,att):
        self.entities=obj
        self.features=att

# Définition d'une classe représentant le treilli de concepts

class ConceptLattice:
    """un treilli de concepts est défini de façon récursive par
    - un noeud-concept
    - un ensemble de treillis descendants"""
    
    def __init__(self,concept):
        self.node=concept
        self.children=[]
    
    def add_child(self,child):
        self.children.append(child)


# Génération aléatoire d'un tableau de taille m x n avec names et movies prédéfinis #

def rand2(n,m):
    return np.random.randint(2, size=(n,m))

def create_tab(n,m):
    [names,movies] = import_xls('data.xls',n,m)
    return pd.DataFrame(rand2(n,m),index=names,columns=movies)

# test
df=create_tab(3,5)
print(df)

# Trouver les concepts formels

# Calcule les objets communs d'un ensemble d'attributs
# i.e. l'ensemble des individus qui ont tous vu tous les films passés en argument

def common_entities(dataframe, attributs):

    ind=list(dataframe.index.values)
    n=len(ind)
    obj=[1 for e in range(n)]

    i=0;
    for e in ind:
        for f in attributs:
            obj[i]=obj[i]*dataframe.loc[e,f]
        i=i+1

    return [ind[i] for i in range(n) if obj[i]==1]

# test
# print('\n')
# res=common_entities(df,["Jaws","Kill Bill","Rambo"])
# print(res)

# Calcule les attributs communs d'un ensemble d'objets
# i.e. l'ensemble des films qui ont tous été vus par les individus passés en argument

def common_features(dataframe, objets):

    col=list(dataframe.columns.values)
    n=len(col)
    att=[1 for e in range(n)]

    i=0;
    for f in col:
        for e in objets:
            att[i]=att[i]*dataframe.loc[e,f]
        i=i+1

    return [col[i] for i in range(n) if att[i]==1]

# test
# print('\n')
# res2=common_features(df,["Bob","Ashley","Jordan"])
# print(res2)


# indique si le couple (objets,attributs) forme un concept formel (résultat booléen)

def is_formal_concept(dataframe,objets,attributs):
    return (attributs==common_features(dataframe,objets))and(objets==common_entities(dataframe,attributs))

# test
# print(is_formal_concept(df,["Bob","Ashley"],(common_features(df,["Bob","Ashley"]))))


# traduit un entier en tableau binaire

def int_to_binary(n):
    if n==0:
        return [[0],0]
    elif n==1:
        return [[1],1]
    else:
        res = int_to_binary(n//2)
        b=n%2
        res[0].insert(0,b)
        res[1]+=b
        return res

# donne toutes les combinaisons possibles de sous-tableau d'un tableau donné

def combinaisons(t):
    t_combi=[]
    n=2**len(t)
    for i in range(n):
        combi=int_to_binary(i)[0]
        t_combi.append([t[i] for i in range(len(combi)) if combi[i]==1])
    return t_combi

# test
# print(combinaisons([0,1,2,3,4,5,6]))

# donne toutes les combinaisons possibles de sous-tableau d'un tableau donné,
# ordonnées par ordre décroissant du nombre d'éléments

def sorted_combinaisons(t):
    
    res=[]
    combi=[]
    n=len(t)
    dic_combi=[[] for i in range(n+1)]
    ncombi=2**n
    
    for i in range(ncombi):
        binary=int_to_binary(i)
        dic_combi[n-binary[1]].append(binary[0])
    
    for e in dic_combi:
        combi=combi+e
        
    for c in combi:
        res.append([t[i] for i in range(len(c)) if c[i]==1])    
    
    return res

#test
# print(sorted_combinaisons([0,1,2,3,4]))

# caculer l'ensemble des concepts formels

def formal_concepts(dataframe):
    
    res=[]
    totalObjets=list(dataframe.index.values)
    aTraiter=sorted_combinaisons(totalObjets)
    
    for e in aTraiter:
        att=common_features(dataframe,e)
        if is_formal_concept(dataframe,e,att):
            res.append(FormalConcept(e,att))
            
    return res

# test
# FC=formal_concepts(df)
# print([(e.entities,e.features) for e in FC])


# indique si le tableau t2 est inclu dans le tableau t1
# prend en argument deux tableau différents et ayant des éléments tous différents
# peut être amélioré (?) en ne considérant que le sous tableau de t1 restant après chaque itération --> voir complexité

def is_included(t1,t2):
    
    res=True
    n1=len(t1)
    n2=len(t2)
    
    if n2 < n1:
        i=0
        while res and i<n2:
            res=res and  (t2[i] in t1)
            i+=1
    
    else:
        res=False
    
    return res

# test
# print(is_included([4,1,2,3],[3,5,2]))

# insère récursivement un concept à sa place dans le treilli par récursion
# si l'ensemble des objets du concept n'est inclu dans aucun enfants de la racine
# on crée un arc entre la racine et le concept
# sinon
# on insère le concept dans les enfants correspondant

def insere_concept_e(concept,treilli):
    
    ch=treilli.children
    arc=True
    ent=concept.entities
    
    for c in ch:
        if is_included(c.node.entities,ent):
            arc=False
            insere_concept_e(concept,c)
    
    if arc:
        treilli.add_child(ConceptLattice(concept))

# construit le treilli de concepts dont la racine est le concept contenant tous
# les objets

def concept_lattice_e(dataframe):
    
    FC=formal_concepts(dataframe)
    FC2=FC[1:]
    res=ConceptLattice(FC[0])
    for concept in FC2:
        insere_concept_e(concept,res)
           
    return res

#test
CL=concept_lattice_e(df)

print("Racine")
print(CL.node.entities)
print(CL.node.features)

for e in CL.children:
    print("Concept suivant")
    print(e.node.entities)
    print(e.node.features)