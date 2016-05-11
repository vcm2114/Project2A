# -*- coding: utf-8 -*-

#-----------#
# Libraries #
#-----------#

import concepts as cp

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

def inobjects(k, obj):
    
    """
    Input : - k: object
            - obj: object list
    Output : boolean: True if k in obj, False otherwise
    """
    
    i = 0
    n = len(obj)
    res = False
    
    while i < n and obj[i] <= k:
        if obj[i] == k:
            res = True
            break
        i += 1
    
    return res

print(inobjects(4, [0, 1, 2, 3, 5, 6, 7, 8, 9]))


# compute the set of last nodes where k appears in the concept lattice

def find_last_occurences(L, k):
    
    """
    Input : - L: concept lattice
            - k: object
    Output : set of the last nodes where k appears
    """
    
    s = set()
    
    for lat in L.children:
        if inobjects(k, lat.node.objects):
            s = s.union({lat})
    
    if len(s) == 0:
        return {L}
    else:
        res = set()
        for lat in s:
            res = res.union(find_last_occurences(lat, k))
        return res

df = cp.create_tab(20,15)
print(df)
A = df.as_matrix()
t = cp.compute_lattice(A)
print(t)
s = find_last_occurences(t, 3)
print(s)