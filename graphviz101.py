# -*- coding: utf-8 -*-

import graphviz
from concepts import *

def add_tail(graph, node, name):
    graph.edge(node,node, taillabel=name,labelangle='90',color='transparent')

def add_head(graph, node, name):
    graph.edge(node,node, headlabel=name,labelangle='270',color='transparent')

def dirgraph(name,nodes,edges,heads,tails):
    dot = graphviz.Digraph(
            name=name,
            graph_attr=dict(rankdir='BT',center='True',margin='0.7',dpi='70',nodesep='1.8',size='10,10'),
            node_attr=dict(shape='circle', width='.25', style='filled', label=''),
            edge_attr=dict(dir='none', labeldistance='1.8', minlen='2',color='#111111',style='setlinewidth(0.5)',fontname='Calibri'),
            format='pdf')
    for n in nodes:
        dot.node(n)
    for e in edges:
        dot.edge(e[0],e[1])
    for h in heads:
        add_head(dot,h[0],h[1])
    for t in tails:
        add_tail(dot,t[0],t[1])
    return dot

# nodes=['1','2','3','4','5','6']
# edges=[['1','2'],['1','3'],['1','4'],['2','5'],['3','6'],['4','5'],['4','6'],['6','5']]
# heads=[['4','Jaws'],['5','SW'],['6','Rambo']]
# tails=[['2','Anne'],['3','Chris - Paul - Gilbert - Anatole'],['4','Bob'],['6','John']]

# dot=dirgraph('firstGraph',nodes,edges,heads,tails)
# dot.render(view=True)

class latticeviz:
        """
        latticeviz class defined by:
        - nodes : nodes array ['1',...,'9']
        - edges : edges array [['1','1'],...,['1','9']]
        - heads : heads array [[node,name],...,['1','Jaws']] (attributes)
        - tails : tails array [[node,name],..,['1','Anne']] (objects)
        - labels  : string array ["objects","attributes"]
        - name    : string
        => For lattice visualization with graphviz.py
        """

        def __init__(self,nodes=[],edges=[],heads=[],tails=[],labels=[],name=""):
            self.nodes=nodes
            self.edges=edges
            self.heads=heads
            self.tails=tails
            self.labels=labels
            self.name=name

        def __str__(self):
            return "name: "+str(self.name)+"\nlabels: "+self.labels[0]+" and "+str(self.labels[1])+"\nnb nodes: "+str(len(self.nodes))+"\nnb edges: "+str(len(self.edges))+"\nnb heads: "+str(len(self.heads))+"\nnb tails: "+str(len(self.tails))

        def digraph(self):
            return dirgraph(self.name,self.nodes,self.edges,self.heads,self.tails)

        def printf(self):
            self.digraph().render(view=True)

        def add_nodes(self,nodes):
            self.nodes.append(nodes)
        def add_edges(self,edges):
            self.edges.append(edges)
        def add_heads(self,heads):
            self.heads.append(heads)
        def add_tails(self,tails):
            self.tails.append(tails)

        def node_exist(self,s_obj,s_attr):
            res_obj=[]
            res_attr=[]
            attr=False
            obj=False
            if not s_attr=='':
                for a in self.heads:
                    if a[1]==s_attr:
                        res_attr.append(a[0])
                        attr=True
            if not s_obj=='':
                for o in self.tails:
                    if o[1]==s_obj:
                        res_obj.append(o[0])
                        obj=True

            if obj and attr:
                for o in res_obj:
                    if o in res_attr:
                        return int(o)
            else:
                if obj:
                    return int(res_obj[0])
                if attr:
                    return int(res_attr[0])
            return 0

def root2viz(df,l,lviz,parent):

    # id of node
    obj_names=obj2name(df,l.node.objects)
    s_o=""
    for o in obj_names:
        s_o=s_o+", "+o

    attr_names=attr2name(df,l.node.attributes)
    s_a=""
    for a in attr_names:
        s_a=s_a+", "+a

    # Add nodes and nodes

    # if root
    if parent==0:
        lviz.nodes=['1']
        n=1

    # if not root
    else:
        exist=lviz.node_exist(s_o[1:],s_a[1:])
        # if node does not exist already
        if exist == 0:
            n=int(lviz.nodes[-1])+1
            lviz.add_nodes(str(n))
            lviz.add_edges([str(parent),str(n)])
        # if node exists -> only add the new edge and stop
        else:
            lviz.add_edges([str(parent),str(exist)])
            return

    # Add tails
    if not s_o[1:]=="":
        lviz.add_tails([str(n),s_o[1:]])

    # Add heads
    if not s_a[1:]=="":
        lviz.add_heads([str(n),s_a[1:]])

    if len(l.children)==0:
        return
    else:
        for c in l.children:
            root2viz(df,c,lviz,n)

# a=latticeviz(nodes,edges,heads,tails,["objet","attributes"],"lattice")
# print(str(a))
# a.printf()


# df1 = create_tab(5,4)
# print(df1)
# M = df1.as_matrix()
# t = compute_lattice(M)
# print("fin lattice \n")
# lviz=latticeviz([],[],[],[],['people','movies'],name="ConceptLattice")
# root2viz(df1,t,lviz,0)
# lviz.printf()
