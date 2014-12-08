__author__ = 'antoniocastro'


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
from datetime import datetime

company_graph = []
people_graph = []

GENERATE_NETWORKS = True
GENERATE_PEOPLE_CLIQUES = False
GENERATE_COMPANY_CLIQUES = True
GENERATE_COMMUNITY_ASSIGNMENTS = True

START_YEAR = 2001
END_YEAR = 2002
STEP_SIZE = 1
k = 2

if GENERATE_NETWORKS:
    # load the edges
    B = []
    for i in range(START_YEAR, END_YEAR+1, STEP_SIZE):
        B.append(nx.Graph())

    with open('relationship_detail.csv') as f:
        reader = csv.reader(f)
        next(reader) # skip the header

        for row in reader:  # Determine networks to add to
            if row[3] == 'NULL':
                start = START_YEAR
            else:
                start = int(row[3][0:4])
                if start < START_YEAR:
                    start = START_YEAR
            if row[4] == 'NULL':
                end = END_YEAR
            else:
                end = int(row[4][0:4])
                if end > END_YEAR:
                    end = END_YEAR

            for i in range(START_YEAR, END_YEAR+1, STEP_SIZE):
                if start <= i and i <= end:
                    B[(i - START_YEAR)/STEP_SIZE].add_edge(int(row[1]), int(row[2]))

    # load the company node list

    company_nodes = []

    with open('public_company_detail.csv') as f:
        reader = csv.reader(f)
        next(reader)  # skip the header
        for row in reader:
            company_nodes.append(int(row[0]))

    # load the person node list

    people_nodes = []

    with open('people_detail.csv') as f:
        reader = csv.reader(f)
        next(reader)  # skip the header
        for row in reader:
            people_nodes.append(int(row[0]))

    # Generate the Projected Collaboration Graphs

    for i in range(START_YEAR, END_YEAR+1, STEP_SIZE):
        B[(i - START_YEAR)/STEP_SIZE].add_nodes_from(people_nodes)
        B[(i - START_YEAR)/STEP_SIZE].add_nodes_from(company_nodes)
        company_graph.append(bipartite.weighted_projected_graph(B[(i - START_YEAR)/STEP_SIZE], company_nodes))
        people_graph.append(bipartite.weighted_projected_graph(B[(i - START_YEAR)/STEP_SIZE], people_nodes))

        nx.write_edgelist(B[(i - START_YEAR)/STEP_SIZE], "relationship_detail" + str(i) + ".edgelist")
        nx.write_edgelist(company_graph[(i - START_YEAR)/STEP_SIZE], "company" + str(i) + ".edgelist")
        nx.write_edgelist(people_graph[(i - START_YEAR)/STEP_SIZE], "people" + str(i) + ".edgelist")

    print "generated graphs for %d" % i

else:
    # for i in range(START_YEAR, END_YEAR + 1):
    for i in range(START_YEAR, END_YEAR + 1, STEP_SIZE):
        print "loading graph: %d" % i
        company_graph.append(nx.read_edgelist("company" + str(i) + ".edgelist", nodetype=int, edgetype=int))
        people_graph.append(nx.read_edgelist("people" + str(i) + ".edgelist", nodetype=int, edgetype=int))

communities = []
if GENERATE_PEOPLE_CLIQUES:
    for i in range(START_YEAR, END_YEAR + 1, STEP_SIZE):

        # get the original bipartite graph for determining company breadth of a network
        B = nx.read_edgelist("relationship_detail" + str(i) + ".edgelist", edgetype=int, nodetype=int)

        print "generating cliques: %d" % i
        communities.append(list(nx.k_clique_communities(people_graph[(i - START_YEAR)/STEP_SIZE], 4)))
        numerator = set()

        # remove cliques below a certain weight that do not project onto a certain number of companies
        intensities = []
        intensities_year = []
        pruned_communities = []
        for community in communities[(i - START_YEAR)/STEP_SIZE]:
            sub_graph = people_graph[(i - START_YEAR)/STEP_SIZE].subgraph(community)
            clique_intensity = 0.0
            company_set = set()
            for edge in sub_graph.edges(data=True):
                clique_intensity += edge[2]['weight']
                company_set = company_set.union(B.neighbors(edge[0]))
                company_set = company_set.union(B.neighbors(edge[1]))
                clique_intensity += len(B.neighbors(edge[0])) + len(B.neighbors(edge[1]))
            clique_intensity = clique_intensity / ((nx.number_of_nodes(sub_graph) + len(company_set)) * ((nx.number_of_nodes(sub_graph)-1) + len(company_set)) / 2)
            if clique_intensity > 1 and len(company_set) >= 2:
                pruned_communities.append(community)
                intensities.append(clique_intensity)

        communities[(i - START_YEAR)/STEP_SIZE] = pruned_communities
        intensities_year.append(intensities)

        for j in range(0, len(communities[(i - START_YEAR)/STEP_SIZE])):
            numerator = numerator.union(list(communities[(i - START_YEAR)/STEP_SIZE][j]))

        coverage = float(len(numerator)) / people_graph[(i - START_YEAR)/STEP_SIZE].number_of_nodes()
        LCC_size = len(nx.connected_components(people_graph[0]).next())
        coverage_LCC = float(len(numerator)) / LCC_size

        print "# of communities: %d" % (len(communities[(i - START_YEAR)/STEP_SIZE]))
        print "coverage of communities: %f" % coverage
        print "size of LCC: %d" % LCC_size
        print "coverage of LCC: %f" % coverage_LCC

        pickle.dump(communities[(i - START_YEAR)/STEP_SIZE], open("communities_" + str((i - START_YEAR)/STEP_SIZE) + ".p", "wb"))
# else:
#     for i in range(START_YEAR, END_YEAR + 1, STEP_SIZE):
#     # for i in [START_YEAR, 2002]:
#         communities.append(pickle.load(open("communities_" + str(i - START_YEAR) + ".p", "rb")))

if GENERATE_COMPANY_CLIQUES:
    for i in range(START_YEAR, END_YEAR + 1, STEP_SIZE):

        # get the original bipartite graph for determining company breadth of a network
        B = nx.read_edgelist("relationship_detail" + str(i) + ".edgelist", edgetype=int, nodetype=int)

        print "generating cliques: %d" % i
        communities.append(list(nx.k_clique_communities(company_graph[(i - START_YEAR)/STEP_SIZE], k)))
        numerator = set()

        # remove cliques below a certain weight that do not project onto a certain number of objects
        intensities = []
        intensities_year = []
        pruned_communities = []
        for community in communities[(i - START_YEAR)/STEP_SIZE]:
            sub_graph = company_graph[(i - START_YEAR)/STEP_SIZE].subgraph(community)
            clique_intensity = 0.0
            for edge in sub_graph.edges(data=True):
                clique_intensity += edge[2]['weight']
            clique_intensity = clique_intensity / (nx.number_of_nodes(sub_graph) * (nx.number_of_nodes(sub_graph)-1) / 2)
            if clique_intensity > 0:
                pruned_communities.append(community)
                intensities.append(clique_intensity)

        communities[(i - START_YEAR)/STEP_SIZE] = pruned_communities
        intensities_year.append(intensities)

        for j in range(0, len(communities[(i - START_YEAR)/STEP_SIZE])):
            numerator = numerator.union(list(communities[(i - START_YEAR)/STEP_SIZE][j]))

        coverage = float(len(numerator)) / people_graph[(i - START_YEAR)/STEP_SIZE].number_of_nodes()
        LCC_size = len(nx.connected_components(people_graph[0]).next())
        coverage_LCC = float(len(numerator)) / LCC_size

        print "# of communities: %d" % (len(communities[(i - START_YEAR)/STEP_SIZE]))
        print "coverage of communities: %f" % coverage
        print "size of LCC: %d" % LCC_size
        print "coverage of LCC: %f" % coverage_LCC

        pickle.dump(communities[(i - START_YEAR)/STEP_SIZE], open("communities_" + str((i - START_YEAR)/STEP_SIZE) + ".p", "wb"))
else:
    for i in range(START_YEAR, END_YEAR + 1, STEP_SIZE):
    # for i in [START_YEAR, 2002]:
        communities.append(pickle.load(open("communities_" + str(i - START_YEAR) + ".p", "rb")))


if GENERATE_COMMUNITY_ASSIGNMENTS: # This is currently a test with just two networks to get everything working

    # get all of the communities in the union of the two V = E U D
    V = nx.Graph()
    V.add_edges_from(people_graph[0].edges(data=True))
    V.add_edges_from(people_graph[1].edges(data=True))

    v_communities = list(nx.k_clique_communities(V, 4))

    for community in v_communities:
        sub_graph = V.subgraph(community)
        clique_intensity = 0.0
        for edge in sub_graph.edges(data=True):
            clique_intensity += edge[2]['weight']
        clique_intensity = clique_intensity / (nx.number_of_nodes(sub_graph) * (nx.number_of_nodes(sub_graph)-1) / 2)
        if clique_intensity > 1:
            pruned_communities.append(community)
        v_communities = pruned_communities

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

        # print "V_k: %d:  %s" % (-1, str(V_k))
        # print "D_k: %d:  %s" % (d_max, str(communities[0][d_max]))
        # print "E_k: %d:  %s" % (e_max, str(communities[1][e_max]))
        # print "-------------"
    print "number of new communities: %d" % len(new_communities)
    print "number of deleted communities : %d" % len(deleted_communities)
    print "number of unchanged communities: %d" % C.values().count(1.0)
    print "Changes:"
    print Counter(C_change.values())
    pickle.dump(C,open("C_START_YEAR-START_YEAR,p", "wb"))
    pickle.dump(C_change, open("C_Change_START_YEAR-2002,p","wb"))



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