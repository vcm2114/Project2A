#
# Quick presentation of basics usage of networkx library (imported as nx)
# ->    networkx enables quick and easy graph structures but also instant integration
# ->    with matplotlib to plot graphs.
#

# --- I. Creating graph and adding nodes and edges --- #

import networkx as nx
import matplotlib.pyplot as plt
G=nx.Graph()

# Nodes add
G.add_node(1)
G.add_nodes_from([2,3])
# Edges add
G.add_edge(1,2)
G.add_edges_from([(3,2),(1,3)])

# Set attributes to a specific node
G.node[1]['names']="Anne"
G.node[1]['movies']=["SW","LOR"]

print("------ Nodes ------")
print(G.number_of_nodes())
print(G.nodes())
print("------ Edges ------")
print(G.number_of_edges())
print(G.edges())
print("------ Neighbors of 1 ------")

print(G.neighbors(1))

print("------ Accessing nodes ------")
print(G[1])
print (G[1]['movies'])

pos = nx.spring_layout(G)
nx.draw_networkx(G, pos)
node_labels = nx.get_node_attributes(G,"names")
nx.draw_networkx_labels(G, pos, labels = node_labels)
plt.show()
