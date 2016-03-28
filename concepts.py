# -*- coding: utf-8 -*-

#---------------#
# Bibliothèques #
#---------------#

# Structures de données
import pandas as pd

# Manipulation de matrices
import numpy as np

# Import de fichier Excel
from xlrd101 import import_xls

# Structure d'arbre de tri
import trie as tr

# Structure de file FIFO
import queue as qu


#---------#
# Classes #
#---------#


# Définition d'une classe concept formel

class FormalConcept:
    """un concept formel est défini par
    - un ensemble d'objets
    - un ensemble d'attributs"""

    """méthode d'initialisation"""
    def __init__(self,obj,att):
        self.objects=obj
        self.attributes=att

    """méthode permettant d'ajouter un objet à un concept"""
    def add_entity(self,entity):
        self.objects.append(entity)

    """méthode permettant d'ajouter un attribut à un concept"""
    def add_feature(self,feature):
        self.attributes.append(feature)

    """méthode facilitant l'affichage console d'un concept"""
    def __str__(self):
        return "Objets : {} | Attributs : {}".format(self.objects, self.attributes)


class Lattice:
    """Un treilli est défini par :
    - un noeud-concept
    - un ensemble de successeurs"""

    """méthode d'initialisation"""
    def __init__(self, c, enfants):
        self.node = c
        self.children = enfants

    """méthode permettant d'ajouter un enfant"""
    def add_child(self, enfant):
        self.children.append(enfant)

    """méthode facilitant l'affichage console d'un concept"""
    def __str__(self):
        return "Noeud : {} \nEnfants : {} \n".format(self.node, self.children)



#------------------------------------#
# Simulation d'un contexte aléatoire #
#------------------------------------#


def rand2(n,m):
    return np.random.randint(2, size=(n,m))

def create_tab(n,m):
    [names,movies] = import_xls('data.xls',n,m)
    return pd.DataFrame(rand2(n,m),index=names,columns=movies)



#--------------------#
# variables globales #
#--------------------#


'''df = create_tab(4,4)
print(df)
A = df.as_matrix()'''

# df1 = pd.DataFrame(
#     {
#     "SW I":[1,1,1,0],
#     "Rambo":[0,0,0,1],
#     "Jaws":[0,1,0,0],
#     "Kill Bill":[1,1,1,1]
#     },
#     index=['Paris', 'Pierre', 'Julien', 'Olivier'])
#
# print(df1)
# M = df1.as_matrix()

def obj2name(df,obj):
    res=[]
    for o in obj:
        res=res+[df.index[o]]
    return res

def attr2name(df,attr):
    res=[]
    for a in attr:
        res=res+[df.columns[a]]
    return res


#---------------------------------------------------#
# Trouver les concepts formels - Algorithme InClose #
#---------------------------------------------------#



# variables globale

r_new=0



# fonction is_cannonical
# prend en argument la matrice des données, des variables r et y,la liste lc des
# concepts formels
# renvoie un booléen indiquant si le concept formel lc[r_new] est canonique ou non
# algorithme développé par S. Andrews (université de Sheffield)

def is_cannonical(mat,r,y,lc):
    global r_new
    res=True
    A=lc[r_new].objects
    B=lc[r].attributes
    k=len(B)-1
    while k >= 0 and res :
        j=y
        while j > B[k] and res :
            h=0
            still=True
            while h < len(A) and still:
                if mat[A[h]][j] == 0:
                    still=False
                h+=1
            if h == len(A) and still:
                res=False
            j-=1
        y=B[k]-1
        k-=1

    j=y
    while j >= 0 and res:
        h=0
        still=True
        while h < len(A):
            if mat[A[h]][j] == 0:
                still=False
            h+=1
        if h == len(A) and still:
            res=False
        j-=1
    return res




# fonction in_close
# prend en argument la matrice de données, des variables r et y initialisées à 0,
# la liste des concepts initialisée à une case contenant l'infimum, le nombre n
# d'attributs
# renvoie la liste de tous les concepts formels, sauf le supremum
# algorithme développé par S. Andrews (université de Sheffield)

def in_close(mat,r,y,lc,n):
    global r_new
    AB=lc[r]
    r_new+=1
    lc.append(FormalConcept([],[]))
    for j in range(y,n):
        lc[r_new].objects=[]
        for i in AB.objects:
            if mat[i][j] == 1:
                lc[r_new].add_entity(i)
        if lc[r_new].objects != [] :
            if len(lc[r_new].objects) == len(AB.objects):
                AB.add_feature(j)
            elif is_cannonical(mat,r,j-1,lc):
                lc[r_new].attributes=AB.attributes+[j]
                in_close(mat,r_new,j+1,lc,n)

# test

# l=[FormalConcept(range(4),[])]
# in_close(M,0,0,l,4)
# for e in l:
#     print(e)
# print(r_new)




#--------------------------------------------------------------------------#
# Trouver les concepts formels et le treillis de concepts - Algorithme DFS #
#--------------------------------------------------------------------------#


# à partir d'un ensemble d'attributs, renvoie tous les objets communs

def common_objects(M, attributs):

    nattributes = len(attributs)
    nobjects = len(M)
    obj = range(nobjects)
    res = [1]*nobjects

    for i in obj:
        j = 0
        while (j < nattributes) and (res[i]==1):
            res[i] = (res[i] and M[i][attributs[j]])
            j += 1

    return [e for e in obj if (res[e]==1)]


# à partir d'un ensemble d'objets, renvoie la liste des attributs communs

def common_attributes(M, objets):

    nobjects = len(objets)
    nattributes = len(M[0])
    att = range(nattributes)
    res = [1]*nattributes

    for j in att:
        i = 0
        while (i < nobjects) and (res[j]==1):
            res[j] = (res[j] and M[objets[i]][j])
            i += 1

    return [e for e in att if (res[e]==1)]


# prend en argument un attribut et une liste d'objets, et renvoie tous les objets
# de cette liste en relation avec l'attribut

def objr(M, att, obj):

    res = []

    for e in obj:
        if M[e,att]:
            res.append(e)

    return res


# prend en argument un objet et une liste d'attributs, et renvoie tous les attributs
# de cette liste en relation avec l'objet

def attrr(M, obj, att):

    res = []

    for e in att:
        if M[obj,e]:
            res.append(e)

    return res

# print(objr(A, 2, [1,2,4]))


# prend en argument la liste de tous les attributs et un échantillon d'attributs
# X, et renvoie L\X

def without(L, X):

    res = []
    Xbis = X+[-1]
    n = len(L)
    i = 0
    j = 0
    while j < n:
        if L[j] == Xbis[i]:
            i += 1
            j += 1
        else:
            res.append(L[j])
            j += 1

    return res


# prend en argument les attributs d'un concepts et renvoie les concepts descendants
# potentiels

def child(M, X):

    res = []

    objX = common_objects(M, X)
    L = without(range(len(M[0])), X)
    t = tr.trie(-1,[],[],[])

    for i in L:
        obji = objr(M, i, objX)
        t.insert_trie(i, obji)

    S = t.equivalence()

    for s in S:
        res.append((s[0], sorted(X+s[1]))) # sorted ?

    return res


# fonction is_closed ===> améliorable <===
# prend en argument un couple renvoyé par la fonction child
# renvoie un booléen indiquant s'il s'agit d'un concept

def is_closed(M, S):
    return len(S[1]) == len(common_attributes(M,S[0]))


# fonction qui prend en argument un couple (obj, attr) et une liste L de treillis
# et indique si le concept formé par le couple est un noeud des lattices de la liste

def ever_existing_lattice(couple, L):

    res = None
    n = len(L)
    i = 0

    while i < n:
        if len(L[i].node.objects) == len(couple[0]):
            if L[i].node.attributes == couple[1]:
                if L[i].node.objects == couple[0]:
                    res = L[i]
                    break
        i += 1

    return res


# fonction qui construit le treilli de Galois d'une matrice donnée
# utilise l'algorithme BFS de Vicky C. Choi (Université de Virginie)

def compute_lattice(M):

    nobj = len(M)
    natt = len(M[0])
    o = list(range(nobj))
    C = FormalConcept(o, common_attributes(M,o))
    L = Lattice(C,[])
    Q = qu.Queue()
    Q.put(L)
    existing = [L]

    while not(Q.empty()):
        lat = Q.get()
        chi = child(M, lat.node.attributes)
        for e in chi:
            if is_closed(M,e):
                K = ever_existing_lattice(e, existing)
                if K == None:
                    K = Lattice(FormalConcept(e[0],e[1]),[])
                    existing.append(K)
                    Q.put(K)
                lat.add_child(K)

    return L

# t = compute_lattice(M)
# print(t)
