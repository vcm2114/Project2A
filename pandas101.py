# -*- coding: utf-8 -*-

#
# Fonctions principales nécessaires au traitement de tables de concept formelle.
#

# Basic imports in pandas
import pandas as pd
import numpy as np
from xlrd101 import import_xls

# -- I. Création de la table -- #

# 1. A la main #
# df1 = pd.DataFrame(
#     {
#     "SW I":[1,0,1,0,1,0],
#     "Kill Bill":[0,1,1,0,1,1],
#     "SAW VI":[1,0,1,0,0,1],
#     "Jaws":[1,0,1,0,0,1],
#     "Rambo":[1,0,1,0,1,1]
#     },
#     index=['Bob','Ashley','John','Paul','Gabby','Jordan'])
#
# print(df1)
# print('\n -------------- \n')

# 2. Avec excel #
def data(n,m,file='Data'):
    df1 = pd.read_excel('data.xlsx',file,header=0,index_col=0)
    return df1.iloc[0:n,0:m]


# 3. Génération semi-aléatoire d'un tableau #
def generate(n):
    return np.random.randint(2, size=n)
#
df3 = pd.DataFrame(
    {
    "SW I":generate(6),
    "Kill Bill":generate(6),
    "SAW VI":generate(6),
    "Jaws":generate(6),
    "Rambo":generate(6)
    },
    index=['Bob','Ashley','John','Paul','Gabby','Jordan'])
#
# print(df3)
# print('\n -------------- \n')

# 4. Génération aléatoire d'un tableau de taille m x n #

def rand2(m,n):
    return np.random.randint(2, size=(m,n))

def create_t(m,n):
    return pd.DataFrame(rand2(m,n),index=(np.arange(m)+1),columns=(np.arange(n)+1))

# 5. Génération aléatoire d'un tableau de taille m x n avec names et movies prédéfinis #

def create_tab(n,m):
    [names,movies] = import_xls('data.xls',n,m)
    return pd.DataFrame(rand2(n,m),index=names,columns=movies)

# dfk=create_tab(3,5)
# print(dfk)
#
# print('\n -------------- \n')
# print('\n -------------- \n')
