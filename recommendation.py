# -*- coding: utf-8 -*-

#-----------#
# Libraries #
#-----------#

# concepts and lattices
import concepts as cp

# queue
import queue as qu

# pandas
import pandas as pd


# compute the support of an attribute list

def support(M,attr):
    """
    Input : - M: context matrix
            - attr: attributes
    Output : |attr(I)''|
    """
    return len(cp.common_objects(M,attr))


# compute the union of the sorted lists attr1 and attr2

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


# compute the support of the association rule attr1 -> attr2

def supp(M,attr1,attr2):
    """
    Input : - M: context matrix
            - attr: attributes
    Output : supp(r) with r: attr1->attr2
    """
    return support(M,union(attr1,attr2))


# indicate if c's attributes are frequent

def frequence(c,th):
    """
    Input : - c: concept
            - th: threshold
    Output : freq(c) (bool)
    """
    return len(c.objects)>=th


# compute the confidence of the association rule attr1 -> attr2

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

# indicate if k is in obj, when obj is a sorted list

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


# compute the set of nodes where k appears and the number of objects is superior to the threshold

def find_occurences(L, k, threshold):

    """
    Input : - L: concept lattice
            - k: object
            - threshold: integer
    Output : set of the nodes where k appears and |objects| >= threshold
    """

    s = set()

    if len(L.node.objects) < threshold:
        return s
    else:
        s = s.union({L})
        for lat in L.children:
            if inobjects(k, lat.node.objects):
                s = s.union(find_occurences(lat, k, threshold))
        return s

# give the elements that are in l2 but not in l1

def extersection(l1, l2):

    """
    Input : - l1, l2: sortedlists of integer
    Output : l2\l1
    """

    n1 = len(l1)
    n2 = len(l2)

    i = 0
    j = 0

    res = []

    while i < n1 and j < n2:
        if l1[i] < l2[j]:
            i += 1
        elif l1[i] > l2[j]:
            res.append(l2[j])
            j += 1
        else:
            i += 1
            j += 1

    if i == n1:
        while j < n2:
            res.append(l2[j])
            j += 1

    return res


# recommender system restricted to a node (give the recommended films near to a given node)

def recommand_node(M, L, k, freq_threshold, conf_threshold):

    """
    Input : - M: formal context
            - L: a node of the concept lattice
            - k: object
            - freq_threshold: integer
            - conf_threshold: float
    Output : list containing the recommanded attributes and the confidence
    """

    Q = qu.Queue()
    done = []
    res = []
    attk = cp.common_attributes(M, [k])

    for lat in L.children:
        if not(inobjects(k, lat.node.objects)):
            Q.put(lat)
            done.append(lat)

    while not(Q.empty()):

        lat = Q.get()
        c = confiance(M, L.node.attributes, lat.node.attributes)

        if frequence(lat.node, freq_threshold) and (c >= conf_threshold):

            exter = extersection(attk, lat.node.attributes)
            for e in exter:
                res.append((e, c))

            proches = []
            for e in lat.children:
                if not(inobjects(k, e.node.objects)):
                    proches.append(e)
            for e in lat.parents:
                if not(inobjects(k, e.node.objects)):
                    proches.append(e)
            for p in proches:
                if not(p in done):
                    done.append(p)
                    Q.put(p)

    return res


# given a list of couples (film, confidence), return a dictionnary where keys are
# the films and the value associated to a key is the max confidence

def purify(l):

    """
    Input : - l: list of couples (film, confidence)
    Output : dictionnary where keys are films and values are max confidences
    """

    res = {}

    for e in l:
        res[e[0]] = max(e[1], res.get(e[0], 0))

    return res


# recommender system

def recommendation(M, L, k, freq_threshold, conf_threshold):

    """
    Input : - M: formal context
            - L: root of the concept lattice
            - k: object
            - freq_threshold: integer
            - conf_threshold: float
    Output : list containing the recommanded attributes and the confidence
    """

    res = []

    nodes = list(find_occurences(L, k, freq_threshold))

    for n in nodes:
        res += recommand_node(M, n, k, freq_threshold, conf_threshold)

    return purify(res)


def recommendation_str(dfs,df,dic,viewer):

    res = ""

    love = []
    middle = []
    hate = []

    movies=df.loc[:, df.loc[viewer] >= 0].columns.tolist()
    films = dfs.columns.tolist()
    res += viewer + " saw"
    for m in movies:
        res += " "
        res += m
        res += ","
    res=res[:-1]
    res += ".\n"

    for e in list(dic.keys()):
        if films[e][0]=="+" and films[e][1:len(films[e])] not in movies:
            love.append((films[e][1:len(films[e])], dic[e]))
        elif films[e][0]=="0" and films[e][1:len(films[e])] not in movies:
            middle.append((films[e][1:len(films[e])], dic[e]))
        elif films[e][1:len(films[e])] not in movies:
            hate.append((films[e][1:len(films[e])], dic[e]))
    if len(love)>0:
        res += viewer + " would certainly like"
        for e in love:
            res += " "
            res += e[0]
            res += " ("
            res += str(round(100*e[1],2))
            res += "%),"
        res=res[:-1]
        res += ".\n"

    if len(middle)>0:
        res += viewer + " could maybe like"
        for e in middle:
            res += " "
            res += e[0]
            res += " ("
            res += str(round(100*e[1],2))
            res += "%),"
        res=res[:-1]
        res += ".\n"

    if len(hate)>0:
        res += viewer + " would not like"
        for e in hate:
            res += " "
            res += e[0]
            res += " ("
            res += str(round(100*e[1],2))
            res += "%),"
        res=res[:-1]
        res += ".\n"
    if len(love)==0 and len(middle)==0 and len(hate)==0:
        res = "No available recommendation for "+viewer + "\n"

    return res



# test

# df = cp.create_tab(30,25)
# print(df)
# A = df.as_matrix()
# t = cp.compute_lattice(A)
# print(t)
# print(30*'-')
# print("Noeuds trouvés :")
# s = find_occurences(t, 3, 3)
# print(s)
#
# r = recommendation(A, t, 3, 3, 0.8)
# print(r)
# rec = recommendation_str(df, r, 0, "John Snow") # r=recommendation, n = nombre de film
# print(rec)
