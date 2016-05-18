# -*- coding: utf-8 -*-

from recommendation import *

def main(df):
    # Find all lattices
    A = df.as_matrix()
    t = compute_lattice(A)

    # Mini UI
    names=df.index
    name=''
    i=0
    print(50*'-')
    while name not in names:
        if i==1:
            print('%s is not a valid name.'%str(name))
        name = input("Name of person to recommend: ")
        type(name)
        i=1
    print(50*'-')

    # Recommendation



df1 = pd.DataFrame(
    {
    "SW I":[1,0,1,0,1,0],
    "Kill Bill":[0,1,1,0,1,1],
    "SAW VI":[1,0,1,0,0,1],
    "Jaws":[1,0,1,0,0,1],
    "Rambo":[1,0,1,0,1,1]
    },
    index=['Bob','Ashley','John','Paul','Gabby','Jordan'])

name = main(df1)
print(name)
