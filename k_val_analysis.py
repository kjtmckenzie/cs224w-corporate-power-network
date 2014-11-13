from collections import defaultdict

__author__ = 'antoniocastro'

import networkx as nx
import matplotlib.pyplot as plt


i = 2001

company_graph = []
people_graph = []

k = 4

print "loading graph: %d" % i
company_graph.append(nx.read_gpickle("company" + str(i) + ".p"))
people_graph.append(nx.read_gpickle("people" + str(i) + ".p"))

histograms = []
for k in range(2, 6):
    print "generating cliques: %d" % i
    communities = (list(nx.k_clique_communities(people_graph[i - 2001], k)))
    numerator = set()

    for j in range(0, len(communities)):
        numerator = numerator.union(list(communities[j]))

    coverage = float(len(numerator)) / people_graph[i - 2001].number_of_nodes()
    LCC_size = len(nx.connected_components(people_graph[0]).next())
    coverage_LCC = float(len(numerator)) / LCC_size
    print "kval = %d" % k
    print "# of communities: %d" % (len(communities))
    print "coverage of communities: %f" % coverage
    print "size of LCC: %d" % LCC_size
    print "coverage of LCC: %f" % coverage_LCC

    community_hist = defaultdict(int)
    for w in list(communities):
        community_hist[len(w)] += 1

    print "average community size: %f" % (len(numerator) / float(len(communities)))

    histograms.append(community_hist)

#for key in sorted(community_hist):
#     print "%d : %d" % (key, community_hist[key])

X0 = histograms[0].keys()
Y0 = histograms[0].values()

X1 = histograms[1].keys()
Y1 = histograms[1].values()

X2 = histograms[2].keys()
Y2 = histograms[2].values()

X3 = histograms[3].keys()
Y3 = histograms[3].values()


plt.loglog(X0, Y0, 'bo', label='k=2')
plt.loglog(X1, Y1, 'ro', label='k=3')
plt.loglog(X2, Y2, 'go', label='k=4')
plt.loglog(X3, Y3, 'yo', label='k=5')
plt.xlim(xmax=500)
plt.title('Community sizes on varying k')
plt.xlabel('community size')
plt.ylabel('number of communities')
plt.legend(loc=0)
plt.show()