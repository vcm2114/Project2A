# Project 2A
Data Science project (French engineering school Mines Nancy) on recommendation systems using Formal Concept Analysis (Unsupervised learning algorithm).
Coded with python and classic py-libraries.

## Introduction
Our project consists of building a recommander system feed by a users rating database. We aim then to recommend to specific individual movies that were positively rated by similar users. It is a collaborative filtering approach.

## Main files
### concepts.py
###### FormalConcept and Lattice class
   Defined classes to handle formal concepts and lattices.
###### In-close algorithm
   To compute formal concepts very quickly.
###### Breadth First Search algorithm
   -  Compute both formal concepts and lattices directly.
   -  Used trie structure for faster implementation (from trie.py).

### recommendation.py
###### recommand_node
   Find the most significant attributes (movies) in term of frequence and confidence.
###### recommendation
   Find all significant nodes with the aimed client to start the recommand_node procedure from.
###### purify
   Select only the most precise recommendations.
###### recommendation_str
   Print recommendations.

### main.py
   -  User input to defined the size of the database imported, the threshold used for frequency and confidance.
   -  Generating the concetps and lattices using concepts.py.
   -  User input to choose the person to recommend to.
   -  Compute recommendation using recommendation.py
   -  Display recommendation

## Other files
### graphviz101.py
   -  Create latticeviz class to visualize lattices using the library graphviz.
### pandas101.py
   Random generation of formal context and excel import of custom database
### scaling.py
   To scale our original rating matrix to a binary table (formal context)
### trie.py
   implementation of trie structure to compute faster lattices in BFS algorithm.
