__author__ = 'antoniocastro'

import cPickle as pickle
import csv


stationarity = pickle.load(open("stationarity.p", "rb"))
communities = pickle.load(open("communities.p", "rb"))
intensities = pickle.load(open("intensities.p", "rb"))
first_appearance = pickle.load(open("first_appearance.p", "rb"))

w = open("stationarity_descriptors.csv", "wb")
writer = csv.writer(w)

with open('public_company_detail.csv') as f:
    reader = csv.reader(f)
    next(reader)  # skip the header
    for row in reader:
        company_node = int(row[0])
        num_communities = 0
        max_intensity = 0
        min_stationarity = 1
        max_stationarity = 0
        average_stationarity = 0
        volatility_of_max_intensity = 0
        relevant_communities = []
        for i in range (0, len(communities[12])):
            if company_node in communities[12][i]:
                num_communities += 1
                relevant_communities.append(i)

        for i in relevant_communities:
            if intensities[12][i] > max_intensity:
                max_intensity = intensities[12][i]
                max_intensity_id = i
            stationarity_i = stationarity[12][i] / (len(stationarity) - first_appearance[12][i])
            if min_stationarity > stationarity_i:
                min_stationarity = stationarity_i
            if max_stationarity < stationarity_i:
                max_stationarity = stationarity_i
            average_stationarity += stationarity_i/len(relevant_communities)
            if i == max_intensity_id:
                volatility_of_max_intensity = stationarity_i
        writer.writerow([company_node, num_communities, max_intensity, min_stationarity, max_stationarity, average_stationarity, volatility_of_max_intensity])

w.close()




