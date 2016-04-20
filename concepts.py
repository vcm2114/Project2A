# -*- coding: utf-8 -*-

#-----------#
# Libraries #
#-----------#

# data structures
import pandas as pd

# matrixes and data analysis
import numpy as np

# import Excel file
from xlrd101 import import_xls

# sorting trees
import trie as tr

# queue FIFO
import queue as qu


#---------#
# Classes #
#---------#


# definition of the formal concept class

class FormalConcept:
    """a formal concept is defined by
    - an object set
    - an attribute set"""

    """initialisation"""
    def __init__(self,obj,att):
        self.objects=obj
        self.attributes=att

    """add an object to the object set"""
    def add_entity(self,entity):
        self.objects.append(entity)

    """add an attribute to the attribute set"""
    def add_feature(self,feature):
        self.attributes.append(feature)

    """print the concept as a string when call the 'print' function"""
    def __str__(self):
        return "Objets : {} | Attributs : {}".format(self.objects, self.attributes)


class Lattice:
    """a lattice is defined by
    - a node (concept)
    - a set of children"""

    """initialisation"""
    def __init__(self, c, enfants):
        self.node = c
        self.children = enfants

    """add a child to the children set"""
    def add_child(self, enfant):
        self.children.append(enfant)

    """print the lattice as a string when call the 'print' function"""
    def __str__(self):
        return "Noeud : {} \nEnfants : {} \n".format(self.node, self.children)



#--------------------------------#
# Simulation of a random context #
#--------------------------------#


def rand2(n,m):
    return np.random.randint(2, size=(n,m))

def create_tab(n,m):
    [names,movies] = import_xls('data.xls',n,m)
    return pd.DataFrame(rand2(n,m),index=names,columns=movies)



#------------------#
# global variables #
#------------------#


df = create_tab(10,5)
print(df)
A = df.as_matrix()
r_new=0

'''df1 = pd.DataFrame(
    {
    "SW I":[1,1,1,0],
    "Rambo":[0,0,0,1],
    "Jaws":[0,1,0,0],
    "Kill Bill":[1,1,1,1]
    },
    index=['Paris', 'Pierre', 'Julien', 'Olivier'])

print(df1)
M = df1.as_matrix()'''

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


#-------------------------------------------------#
# Find the formal concept set - InClose algorithm #
#-------------------------------------------------#



# is_cannonical function
# point if lc[r_new] is canonical
# algorithm from S. Andrews (Sheffield University)

def is_cannonical(mat,r,y,lc):
    
    """
    Input: - mat: context matrix
           - r: integer, number of concepts already computed
           - y: integer, parameter
           - lc: list of concepts
    Output: - res: boolean
    """
    
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




# in_close function
# recursive function
# compute the list of concepts in lexicographical order
# algorithm from S. Andrews (Sheffield University)

def in_close(mat,r,y,lc,n):
    
    """
        Input: - mat: context matrix
               - r: integer, number of concepts already computed, initialised at 0
               - y: integer, parameter initialised at 0
               - lc: list of concepts initialised at []
               - n: integer, number of attributes in the context
        Output: - None (lc is mutated)
    """    
    
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

'''l=[FormalConcept(range(4),[])]
in_close(M,0,0,l,4)
for e in l:
    print(e)
print(r_new)'''




#--------------------------------------------------------------------#
# Find the set formal concepts and built the lattice - DFS algorithm #
#--------------------------------------------------------------------#


# compute the set of objects that are in relation with the given set of attributes

def common_objects(M, attributs):
    
    '''
    Input: - M: context matrix
           - attributs: a set of attributes
    Output: set of common objects
    '''

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


# compute the set of attributes that are in relation with the given set of objects

def common_attributes(M, objets):
    
    '''
    Input: - M: context matrix
           - objets: a set of objects
    Output: set of common attributes
    '''

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


# compute the set of objects beyond a given subset in relation with a single given attribute

def objr(M, att, obj):
    
    """
    Input: - M: context matrix
           - att: given attribute
           - obj: subset of objects
    Output: res, subset of obj
    """

    res = []

    for e in obj:
        if M[e,att]:
            res.append(e)

    return res


# compute the set of attributes beyond a given subset in relation with a single given object

def attrr(M, obj, att):
    
    """
    Input: - M: context matrix
            - obj: given aobject
            - att: subset of attributes
    Output: res, subset of att
    """    

    res = []

    for e in att:
        if M[obj,e]:
            res.append(e)

    return res


# compute L\X

def without(L, X):
    
    """
    Input: - L: list
           - X: list
    Output: res = L\X
    """

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


# compute the list of potential children of the concept whose set of attributes is X

def child(M, X):
    
    """
    Input: - M: context matrix
           - X: list of attributes
    Output: - res: list of potential children (obj, att)
    """

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


# is_closed function ===> can be improved <===
# point if the given couple S is a formal concept

def is_closed(M, S):
    
    """
    Input: - M: context matrix
           - S: couple (obj, att)
    Output: boolean
    """
    
    return len(S[1]) == len(common_attributes(M,S[0]))


# if the given couple represents a concept that already exists, return the concept,
# otherwise return None

def ever_existing_lattice(couple, L):
    
    """
    Input: - couple: couple (obj, att)
           - L: lattice
    Output: res, None or already-existing concept
    """

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


# Compute the lattice associated to a given context
# BFS algorithm from Vicky C. Choi (Virginia Tech University)

def compute_lattice(M):
    
    """
    Input: - M: context matrix
    Output: - L: lattice
    """

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

# test

"""t = compute_lattice(A)
print(t)"""