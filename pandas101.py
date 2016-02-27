#
# Fonctions principales nécessaires au traitement de tables de concept formelle.
#

# Basic imports in pandas
import pandas as pd
import numpy as np
from xlrd101 import import_xls

# -- I. Création de la table -- #

# 1. A la main #
df1 = pd.DataFrame(
    {
    "SW I":[1,0,1,0,1,0],
    "Kill Bill":[0,1,1,0,1,1],
    "SAW VI":[1,0,1,0,0,1],
    "Jaws":[1,0,1,0,0,1],
    "Rambo":[1,0,1,0,1,1]
    },
    index=['Bob','Ashley','John','Paul','Gabby','Jordan'])

print(df1)
print('\n -------------- \n')

# 2. Avec excel #
df2 = pd.read_excel('data.xls',sheetname='data')
print(df2)
print('\n -------------- \n')

# 3. Génération semi-aléatoire d'un tableau #
def generate(n):
    return np.random.randint(2, size=n)

df3 = pd.DataFrame(
    {
    "SW I":generate(6),
    "Kill Bill":generate(6),
    "SAW VI":generate(6),
    "Jaws":generate(6),
    "Rambo":generate(6)
    },
    index=['Bob','Ashley','John','Paul','Gabby','Jordan'])

print(df3)
print('\n -------------- \n')

# 4. Génération aléatoire d'un tableau de taille m x n #

def rand2(m,n):
    return np.random.randint(2, size=(m,n))

def create_t(m,n):
    return pd.DataFrame(rand2(m,n),index=(np.arange(m)+1),columns=(np.arange(n)+1))

df4 = create_t(10,10)

print(df4)
print('\n -------------- \n')
print('\n -------------- \n')

# 5. Génération aléatoire d'un tableau de taille m x n avec names et movies prédéfinis #

def create_tab(n,m):
    [names,movies] = import_xls('data.xls',n,m)
    return pd.DataFrame(rand2(n,m),index=names,columns=movies)

dfk=create_tab(3,5)
print(dfk)

print('\n -------------- \n')
print('\n -------------- \n')

# -- II. Formal Concept with table -- #

df=pd.DataFrame(
    {
    "SW I":generate(6),
    "Kill Bill":generate(6),
    "SAW VI":generate(6),
    "Jaws":generate(6),
    "Rambo":generate(6)
    },
    index=['Bob','Ashley','John','Paul','Gabby','Jordan'])
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
            obj[i]=obj[i]*df.loc[e,f]
        i=i+1

    return [ind[i] for i in range(n) if obj[i]==1]

print('\n')
res=common_entities(df,["Jaws","Kill Bill","Rambo"])
print(res)

# Calcule les attributs communs d'un ensemble d'objets
# i.e. l'ensemble des films qui ont tous été vus par les individus passés en argument

def common_features(dataframe, objets):

    col=list(dataframe.columns.values)
    n=len(col)
    att=[1 for e in range(n)]

    i=0;
    for f in col:
        for e in objets:
            att[i]=att[i]*df.loc[e,f]
        i=i+1

    return [col[i] for i in range(n) if att[i]==1]

print('\n')
res2=common_features(df,["Bob","Ashley","Jordan"])
print(res2)


# indique si le couple (objets,attributs) forme un concept formel (résultat booléen)

def is_formal_concept(dataframe,objets,attributs):
    return (attributs==common_features(dataframe,objets))and(objets==common_entities(dataframe,attributs))

print(is_formal_concept(df,["Bob","Ashley"],(common_features(df,["Bob","Ashley"]))))


# à partir d'un tableau, renvoie l'ensemble des sous-tableau contenant une case de moins

def subtable(t):
    n=len(t)
    return [t[0:i]+t[i+1:] for i in range(n-1)]+[t[0:n-1]]

print(subtable([1,2,3,4,5,6]))

# traduit un entier en tableau binaire

def int_to_binary(n):
    if n==0:
        return [0]
    elif n==1:
        return [1]
    else:
        res = int_to_binary(n//2)
        res.insert(0,n%2)
        return res

# donne toutes les combinaisons possibles de sous-tableau d'un tableau donné

def combinaisons(t):
    res=[]
    n=2**len(t)
    for i in range(n):
        combi=int_to_binary(i)
        res.append([t[i] for i in range(len(combi)) if combi[i]==1])
    return res

print(combinaisons([0,1,2,3,4,5,6]))

# caculer l'ensemble des concepts formels

def formal_concepts(dataframe):
    res=[]
    totalObjets=list(dataframe.index.values)
    aTraiter=combinaisons(totalObjets)
    while aTraiter != [] :
        obj=aTraiter[0]
        att=common_features(dataframe,obj)
        if is_formal_concept(dataframe,obj,att):
            res.append((obj,att)) # comment enrgistrer l'ancetre ?
        aTraiter.remove(obj)
    return res

print(formal_concepts(df))