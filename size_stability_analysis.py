__author__ = 'antoniocastro'

import cPickle as pickle
from collections import defaultdict
import matplotlib.pyplot as plt


C = pickle.load(open("C_2001-2001,p", "rb"))
C2 = pickle.load(open("C_2001-2013,p", "rb"))
community_1 = pickle.load(open("communities_0.p", "rb"))
community_2 = pickle.load(open("communities_1.p", "rb"))
community_3 = pickle.load(open("communities_12.p", "rb"))


#C_Change = pickle.load(open("C_Change_2001-2002.p"))

size_change_hist = defaultdict(int)
size_change_hist2 = defaultdict(int)

size_hist = defaultdict(float)

X_DECAY = []
Y_DECAY = []
X_DECAY2 = []
Y_DECAY2 = []

for a,b in C:
    size_hist[len(community_1[a])]+= 1

for a,b in C:
    if C[(a,b)] < 1:
        size_change_hist[len(community_1[a])] += 1/size_hist[len(community_1[a])]
        X_DECAY.append(len(community_1[a]))
        Y_DECAY.append(1-C[(a,b)])


size_change_hist_2 = defaultdict(int)
for a,b in C2:
    if C2[(a,b)] < 1:
        size_change_hist2[len(community_1[a])] += 1/size_hist[len(community_1[a])]
        X_DECAY2.append(len(community_1[a]))
        Y_DECAY2.append(1-C2[(a,b)])

X = size_change_hist.keys()
Y = size_change_hist.values()

X2 = size_change_hist2.keys()
Y2 = size_change_hist2.values()

plt.plot(X, Y, 'yo', label="2001-2002")
plt.plot(X2, Y2, 'bo', label="2001-2013")
plt.xlim(xmax=300)
plt.title('Community sizes on varying k')
plt.xlabel('community size')
plt.ylabel('% communities with change in auto_correlation')
plt.legend(loc=0)
plt.show()

plt.plot(X_DECAY,Y_DECAY, 'yo', label="2001-2002")
plt.plot(X_DECAY2,Y_DECAY2, 'bo', label="2001-2013")
plt.title("magnititude of decay")
plt.xlabel("community size")
plt.ylabel("1-C")
plt.legend(loc=0)
plt.show()



print "hi"