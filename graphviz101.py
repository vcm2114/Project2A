# -*- coding: utf-8 -*-

# Thanks to http://matthiaseisen.com/articles/graphviz/

import graphviz

def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph

def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph

def add_tail(graph, node, name):
    graph.edge(node,node, taillabel=name,labelangle='90',color='transparent')

def add_head(graph, node, name):
    graph.edge(node,node, headlabel=name,labelangle='270',color='transparent')

def dirgraph(name,nodes,edges,heads,tails):
    dot = graphviz.Digraph(
            name=name,
            graph_attr=dict(rankdir='BT',center='True',margin='0.7',dpi='70',nodesep='0.8',size='10,10'),
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

nodes=['1','2','3','4','5','6']
edges=[['1','2'],['1','3'],['1','4'],['2','5'],['3','6'],['4','5'],['4','6'],['6','5']]
heads=[['4','Jaws'],['5','SW'],['6','Rambo']]
tails=[['2','Anne'],['3','Chris - Paul - Gilbert - Anatole'],['4','Bob'],['6','John']]

# dot=dirgraph('firstGraph',nodes,edges,heads,tails)
# dot.render(view=True)

class latticeviz:
        """
        latticeviz class defined by:
        - nodes : nodes array [['1'],...,['9']]
        - edges : edges array [['1','1'],...,['1','9']]
        - heads : heads array [[node,name],...,['1','Jaws']] (attributes)
        - tails : tails array [[node,name],..,['1','Anne']] (objects)
        - labels  : string array ["objects","attributes"]
        - name    : string
        => For lattice visualization with graphviz.py
        """

        def __init__(self,nodes,edges,heads,tails,labels,name):
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

a=latticeviz(nodes,edges,heads,tails,["objet","attributes"],"lattice")
print(str(a))
a.printf()

#
# print(g3.source)
#
# filename = g3.render(filename=file)
# print filename
# import subprocess           # to execute bash
# bashCommand = "open "+file+".png"
# output = subprocess.check_output(['bash','-c', bashCommand])
