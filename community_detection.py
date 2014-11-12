from collections import defaultdict

__author__ = 'antoniocastro'

import networkx as nx
import csv
import networkx.algorithms.bipartite as bipartite
import matplotlib.pyplot as plt
import cPickle as pickle
import itertools
import operator
from collections import Counter

company_graph = []
people_graph = []

GENERATE = False
GENERATE_CLIQUE = False
GENERATE_COMMUNITY_ASSIGNMENTS = True
k = 2

if GENERATE:
    for i in range(2001, 2014):
        # for i in [2001, 2002, 2003]:

        # load the edges
        B = nx.read_edgelist("relationship_detail_" + str(i) + ".csv", delimiter=',', nodetype=int)

        # load the company node list

        company_nodes = []

        with open('public_company_detail.csv') as f:
            reader = csv.reader(f)
            next(reader)  # skip the header
            for row in reader:
                company_nodes.append(int(row[0]))
            B.add_nodes_from(company_nodes)

        # load the person node list

        people_nodes = []

        with open('people_detail.csv') as f:
            reader = csv.reader(f)
            next(reader)  # skip the header
            for row in reader:
                people_nodes.append(int(row[0]))
            B.add_nodes_from(people_nodes)

        company_graph.append(bipartite.weighted_projected_graph(B, company_nodes))
        people_graph.append(bipartite.weighted_projected_graph(B, people_nodes))
        nx.write_gpickle(company_graph[i - 2001], "company" + str(i) + ".p")
        nx.write_gpickle(people_graph[i - 2001], "people" + str(i) + ".p")

        print "generated graphs for %d" % i

else:
    # for i in range(2001, 2014):
    for i in [2001, 2002, 2003]:
        print "loading graph: %d" % i
        company_graph.append(nx.read_gpickle("company" + str(i) + ".p"))
        people_graph.append(nx.read_gpickle("people" + str(i) + ".p"))

communities = []
if GENERATE_CLIQUE:
    for i in range(2001, 2014):

        print "generating cliques: %d" % i
        communities.append(list(nx.k_clique_communities(people_graph[i - 2001], 4)))
        numerator = set()

        for j in range(0, len(communities[i - 2001])):
            numerator = numerator.union(list(communities[i - 2001][j]))

        coverage = float(len(numerator)) / people_graph[i - 2001].number_of_nodes()
        LCC_size = len(nx.connected_components(people_graph[0]).next())
        coverage_LCC = float(len(numerator)) / LCC_size

        print "# of communities: %d" % (len(communities[i - 2001]))
        print "coverage of communities: %f" % coverage
        print "size of LCC: %d" % LCC_size
        print "coverage of LCC: %f" % coverage_LCC

        pickle.dump(communities[i - 2001], open("communities_" + str(i - 2001) + ".p", "wb"))
else:
    # for i in range(2001, 2014):
    for i in [2001, 2002, 2003]:
        communities.append(pickle.load(open("communities_" + str(i - 2001) + ".p", "rb")))


if GENERATE_COMMUNITY_ASSIGNMENTS: # This is currently a test with just two networks to get everything working
    # get all of the communities in the union of the two V = E U D

    V = nx.Graph()
    V.add_edges_from(people_graph[0].edges())
    V.add_edges_from(people_graph[1].edges())

    v_communities = list(nx.k_clique_communities(V, 4))

    matches = []
    new_communities = []
    deleted_communities = []
    C = defaultdict(float)
    C_size_before = defaultdict(int)
    C_size_after = defaultdict(int)
    C_change = defaultdict(int)

    # find the candidate communities for matching from E and D

    for V_k in list(v_communities):
        D_candidates = []
        E_candidates = []
        for D_i in range(0, len(list(communities[0]))):
            if set(communities[0][D_i]).issubset(V_k):
                D_candidates.append(D_i)
        for E_i in range(0, len(list(communities[1]))):
            if set(communities[1][E_i]).issubset(V_k):
                E_candidates.append(E_i)

    # match and rank, find new and deleted communities
        match_candidates = list(itertools.product(D_candidates, E_candidates))
        match_ranks = defaultdict(float)
        if len(match_candidates) > 0:
            for d,e in match_candidates:
                match_ranks[(d, e)] = float(len(communities[0][d] & communities[1][e]))/len(communities[0][d] | communities[1][e])
            d_max, e_max = (max(match_ranks.iteritems(), key=operator.itemgetter(1))[0])
            matches.append((d_max, e_max))
            C[(d_max, e_max)] = match_ranks[d_max, e_max]
            C_size_before[(d_max, e_max)] = len(communities[0][d_max])
            C_size_after[(d_max, e_max)] = len(communities[1][e_max])
            C_change[(d_max, e_max)] = C_size_after[(d_max, e_max)] - C_size_before[(d_max, e_max)]
        else:
            if len(D_candidates) == 0:
                new_communities.append(E_candidates[0])
            if len(E_candidates) == 0:
                deleted_communities.append(D_candidates[0])

        print "V_k: %d:  %s" % (-1, str(V_k))
        print "D_k: %d:  %s" % (d_max, str(communities[0][d_max]))
        print "E_k: %d:  %s" % (e_max, str(communities[1][e_max]))
        print "-------------"
    print "number of new communities: %d" % len(new_communities)
    print "number of deleted communities : %d" % len(deleted_communities)
    print "number of unchanged communities: %d" % C.values().count(1.0)
    print "Changes:"
    print Counter(C_change.values())



    # graph of change vs. size
    # d3?



# community_hist = defaultdict(int)
# for w in list(communities[0]):
#     community_hist[len(w)] += 1
#
# for key in sorted(community_hist):
# #     print "%d : %d" % (key, community_hist[key])
# plt.loglog(community_hist.values())
# plt.show()