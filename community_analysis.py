__author__ = 'antoniocastro'

import cPickle as pickle
import networkx as nx

people = nx.Graph()

community = pickle.load(open("communities_0.p", "rb"))

f = open("2001_communities.txt", "wb")
for item in community:
    f.write("%s\n" % item)
f.close()

people = pickle.load(open("people2001.p", "rb"))

for edge in people.edges(data=True):
    if edge[2]['weight'] < 2:
        people.remove_edge(edge[0], edge[1])

f = open("people2001.txt", "wb")
for item in people:
    f.write("%s\n" % item)
f.close()