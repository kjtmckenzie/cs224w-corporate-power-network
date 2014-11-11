__author__ = 'antoniocastro'

import networkx as nx
import csv
import networkx.algorithms.bipartite as bipartite
import matplotlib.pyplot as plt
import pickle

company_graph = []
people_graph = []

GENERATE = True

if GENERATE:
    for i in range(2001, 2014):

        # load the edges
        B = nx.read_edgelist("relationship_detail_" + str(i) + ".csv", delimiter=',', nodetype=int)

        # load the company node list

        company_nodes=[]

        with open('public_company_detail.csv') as f:
            reader = csv.reader(f)
            next(reader) # skip the header
            for row in reader:
                company_nodes.append(int(row[0]))
            B.add_nodes_from(company_nodes)

        # load the person node list

        people_nodes=[]

        with open('people_detail.csv') as f:
            reader = csv.reader(f)
            next(reader) # skip the header
            for row in reader:
                people_nodes.append(int(row[0]))
            B.add_nodes_from(people_nodes)

        company_graph.append(bipartite.weighted_projected_graph(B,company_nodes))
        people_graph.append(bipartite.weighted_projected_graph(B,people_nodes))
        nx.write_gpickle(company_graph[i-2001], "company" + str(i) + ".p")
        nx.write_gpickle(people_graph[i-2001], "people" + str(i) + ".p")

        print "generated graphs for %d" % (i)

else:
    for i in range(2001, 2014):
        company_graph.append(nx.read_gpickle("company" + str(i) + ".p"))
        people_graph.append(nx.read_gpickle("people" + str(i) + ".p"))



