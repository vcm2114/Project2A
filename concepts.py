import pandas as pd
import numpy as np
from xlrd101 import import_xls

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



#------------------------------------#
# Simulation d'un contexte aléatoire #
#------------------------------------#


def rand2(n,m):
    return np.random.randint(2, size=(n,m))

def create_tab(n,m):
    [names,movies] = import_xls('data.xls',n,m)
    return pd.DataFrame(rand2(n,m),index=names,columns=movies)
    


# variables globales
df = create_tab(5,5)
print(df)
A = df.as_matrix()



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

'''l=[FormalConcept(range(5),[])]
in_close(A,0,0,l,5)
for e in l:
    print(e)
print(r_new)'''



#--------------------------------------------------------------------------#
# Trouver les concepts formels et le treillis de concepts - Algorithme DFS #
#--------------------------------------------------------------------------#

# à partir  d'un ensemble d'attributs, renvoie tous les objets communs

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

print(objr(A, 2, [1,2,4]))


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