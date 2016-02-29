from concepts import *  # Import pandas and numpy
import networkx as nx
import matplotlib.pyplot as plt

# Tests random

df = create_tab(6,5)
print(df)

fc = formal_concepts(df)
print(fc)

# Auxiliary functions

# Sort in increasing order for objects of a formal concept array
def sort_fc(fc):
    return fc
