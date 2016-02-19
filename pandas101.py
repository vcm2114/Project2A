# Basic import in pandas
import pandas as pd
import numpy as np

### -- I - Création de la table -- ###

## 1. A la main ##
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

## 2. Avec excel ##
df2 = pd.read_excel('data.xls',sheetname='data')
print(df2)
print('\n -------------- \n')

## 3. Génération semi-aléatoire d'un tableau ##
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

## 4. Génération aléatoire d'un tableau de taille m x n ##

def rand2(m,n):
    return np.random.randint(2, size=(m,n))

def create_tab(m,n):
    return pd.DataFrame(rand2(m,n),index=(np.arange(m)+1),columns=(np.arange(n)+1))

df4 = create_tab(10,10)

print(df4)
print('\n -------------- \n')
