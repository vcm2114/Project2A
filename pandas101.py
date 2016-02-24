#
# Fonctions principales nécessaires au traitement de tables de concept formelle.
#

# Basic imports in pandas
import pandas as pd
import numpy as np

# -- I - Création de la table -- #

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

def create_tab(m,n):
    return pd.DataFrame(rand2(m,n),index=(np.arange(m)+1),columns=(np.arange(n)+1))

df4 = create_tab(10,10)

print(df4)
print('\n -------------- \n')
print('\n -------------- \n')
print('\n -------------- \n')
print('\n -------------- \n')

# -- II - Modification de la table -- #

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

# Calcule le concept formel d'un ensemble d'attributs
# i.e. l'ensemble des individus qui ont tous vu tous les films passés en argument

def concept_formel_attribut(dataframe, attributs):
    
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
res=concept_formel_attribut(df,["Jaws","Kill Bill","Rambo"])
print(res)

# Calcule le concept formel d'un ensemble d'objets
# i.e. l'ensemble des films qui ont tous été vus par les individus passés en argument

def concept_formel_objet(dataframe, objets):
    
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
res2=concept_formel_objet(df,["Bob","Ashley","Jordan"])
print(res2)