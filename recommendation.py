# -*- coding: utf-8 -*-

#-----------#
# Libraries #
#-----------#

from concepts import *

def support(M,attr):
    """
    Input : - M: context matrix
            - attr: attributes
    Output : |attr(I)''|
    """
    return len(common_objects(M,attr))

def union(attr1,attr2):
    """
    Input : - attr1: set of attributes
            - attr2: set of attributes
    Output : - union of attr1 & attr2
    """
    i=0
    j=0
    union=[]
    # find union of attr1 and attr2
    while i<len(attr1) and j<len(attr2):
        if attr1[i]==attr2[j]:
            union.append(attr1[i])
            i+=1
            j+=1
        elif attr1[i] < attr2[j]:
            union.append(attr1[i])
            i+=1
        else:
            union.append(attr2[j])
            j+=1
    if i>=(len(attr1)-1):
        while j<len(attr2):
            union.append(attr2[j])
            j+=1

    if j>=(len(attr2)-1):
        while i<len(attr1):
            union.append(attr1[i])
            i+=1
    return union

def supp(M,attr1,attr2):
    """
    Input : - M: context matrix
            - attr: attributes
    Output : supp(r) with r: attr1->attr2
    """
    return support(M,union(attr1,attr2))

def frequence(c,th):
    """
    Input : - c: concept
            - th: threshold
    Output : freq(c) (bool)
    """
    return len(c.objects)>=th

def confiance(M,attr1,attr2):
    """
    Input : - M: context matrix
            - attr1: attributes 1
            - attr2: attributes 2
    Output : conf(r) ith r: attr1->attr2
    """
    return supp(M,attr1,attr2)/support(M,attr1)


# test
'''
df1 = create_tab(10,10)
print(df1)
M = df1.as_matrix()
l=[FormalConcept(range(10),[])]
in_close(M,0,0,l,10)
print(l[3])
print(l[4])
print(supp(M,l[3].attributes,l[4].attributes))
'''
