# -*- coding: utf-8 -*-

from concepts import *
from recommendation import *
from scaling import *
from pandas101 import *

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


df = scaling(data(8,5))
print(df)



