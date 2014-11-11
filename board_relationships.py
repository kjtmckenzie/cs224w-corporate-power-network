import snap
import random
import time
import sys
import csv
import os
import operator


# the returned relationship has the following 4 items in each row i:
# relationships[i][0] = Board Member ID
# relationships[i][1] = Board Member First Name
# relationships[i][2] = Board Member Last Name
# relationships[i][3] = Standardized Company Name in 896 companies
# relationships[i][4] = Standardized Company ID
#
# all_directors is a dictionary of Board Member ID -> Board Member Name
# all_companies is a dictionary of Company ID -> Company Name
def parseInputFile(path):
    relationships = []
    try:
        f = open(path, 'rt')
        reader = csv.reader(f)
        for row in reader:
            relationships.append(row)
    finally:
        f.close()
    
    #remove the column names
    relationships.pop(0)
    
    all_directors = {} #dictionary of ID -> Name for people
    all_companies = {} #dictionary of ID -> Name for companies
    
    for i in xrange(len(relationships)):
        director_id = str(relationships[i][0])
        first_name = str(relationships[i][1])
        last_name = str(relationships[i][2])
        company_name = str(relationships[i][3])
        company_id = str(relationships[i][4])
        if director_id not in all_directors.keys():
            all_directors[director_id] = first_name + " " + last_name
        if company_id not in all_companies:
            all_companies[company_id] = company_name

    return relationships, all_directors, all_companies
    



def initDirectorNetwork(relationships, all_directors, all_companies):
    director_network = snap.TUNGraph.New()
    
    edge_dict = {}
    
    #add all directors
    for key, value in all_directors.iteritems():
        director_network.AddNode(int(key))
    
    num_iterations = len(relationships)
    itercounter = 0
    #create relationships list
    for i in relationships:
        if (itercounter % 1000 == 0):
            print "On iteration %d of %d" % (itercounter, num_iterations)
        for j in relationships:
            id1 = int(i[0])
            id2 = int(j[0])
            comp1 = i[3]
            comp2 = j[3]
            if (id1 < id2) and (comp1 == comp2):
                director_network.AddEdge(id1, id2)
                edge_name = str(id1) + " to " + str(id2)
                if edge_name in edge_dict:
                    edge_dict[edge_name] = edge_dict[edge_name] + 1
                else:
                    edge_dict[edge_name] = 1
        itercounter += 1

    return director_network, edge_dict  
    
def saveDirectorNetwork(director_network, dir_edge_dict):
    print "Printing Director network to ./director_network.graph"
    FOut = snap.TFOut("director_network.graph")
    director_network.Save(FOut)
    FOut.Flush()

    writer = csv.writer(open('dir_edge_dict.csv', 'wb'))
    for key, value in dir_edge_dict.items():
       writer.writerow([key, value])
    
def loadDirectorNetwork(relationships, all_directors, all_companies):
    if (os.path.isfile("director_network.graph") and 
            os.path.isfile("dir_edge_dict.csv")):
        print "Loading Director Network from Disk"
        FIn = snap.TFIn("director_network.graph")
        director_network = snap.TUNGraph.Load(FIn)
        
        reader = csv.reader(open('dir_edge_dict.csv', 'rb'))
        dir_edge_dict = dict(x for x in reader)
    else:
        print "Generating Director Network (this may take a couple minutes)"
        director_network, dir_edge_dict = initDirectorNetwork(relationships, all_directors, all_companies)
        saveDirectorNetwork(director_network, dir_edge_dict)
        
    return director_network, dir_edge_dict

def initCorporationNetwork(relationships, all_directors, all_companies):
    corporation_network = snap.TUNGraph.New()
    
    edge_dict = {}
    company_name_dict = {}
    
    #add all companies
    for key, value in all_companies.iteritems():
        corporation_network.AddNode(int(key))
    
    num_iterations = len(relationships)
    itercounter = 0
    #create relationships list
    for i in relationships:
        if (itercounter % 1000 == 0):
            print "On iteration %d of %d" % (itercounter, num_iterations)
        for j in relationships:
            id1 = int(i[0])
            id2 = int(j[0])
            comp1 = int(i[4])
            comp2 = int(j[4])
            if (id1 == id2) and (comp1 < comp2):
                corporation_network.AddEdge(comp1, comp2)
                edge_name = str(comp1) + " to " + str(comp2)
                if edge_name in edge_dict:
                    edge_dict[edge_name] = edge_dict[edge_name] + 1
                else:
                    edge_dict[edge_name] = 1
        itercounter += 1

    return corporation_network, edge_dict  

def saveCorporationNetwork(corporation_network, corp_edge_dict):
    print "Printing Corporation Network to ./corporation_network.graph"
    FOut = snap.TFOut("corporation_network.graph")
    corporation_network.Save(FOut)
    FOut.Flush()

    writer = csv.writer(open('corp_edge_dict.csv', 'wb'))
    for key, value in corp_edge_dict.items():
       writer.writerow([key, value])
    
def loadCorporationNetwork(relationships, all_directors, all_companies):
    if (os.path.isfile("corporation_network.graph") and 
            os.path.isfile("corp_edge_dict.csv")):
        print "Loading Corporation Network from Disk"
        FIn = snap.TFIn("corporation_network.graph")
        corporation_network = snap.TUNGraph.Load(FIn)
        
        reader = csv.reader(open('corp_edge_dict.csv', 'rb'))
        corp_edge_dict = dict(x for x in reader)
    else:
        print "Generating Corporation Network (this may take a couple minutes)"
        corporation_network, corp_edge_dict = initCorporationNetwork(relationships, all_directors, all_companies)
        saveCorporationNetwork(corporation_network, corp_edge_dict)
        
    return corporation_network, corp_edge_dict

    

def getCentralNodes(graph, num_most_central, name_dict):
    MxWcc = snap.GetMxWcc(graph)
    node_centrality_dict = {}
    
    # Only include nodes in the largest connected component
    for NI in MxWcc.Nodes():
        node_closeness = snap.GetClosenessCentr(graph, NI.GetId())
        node_name = name_dict[str(NI.GetId())]
        node_centrality_dict[node_name] = node_closeness
        
    sorted_dict = sorted(node_centrality_dict.items(), key=operator.itemgetter(1), reverse=True)
    
    for i in xrange(num_most_central):
        print "%d. Node: %s, Centrality: %f" % (i + 1, sorted_dict[i][0], sorted_dict[i][1])
    

def getHighestNodeDegrees(graph, num_highest_degree, name_dict):
    node_degree_dict = {}
    
    # Only include nodes in the largest connected component
    for NI in graph.Nodes():
        node_degree = NI.GetDeg()
        node_name = name_dict[str(NI.GetId())]
        node_degree_dict[node_name] = node_degree
    
    sorted_dict = sorted(node_degree_dict.items(), key=operator.itemgetter(1), reverse=True)
    
    for i in xrange(num_highest_degree):
        print "%d. Node: %s, Degree: %d" % (i + 1, sorted_dict[i][0], sorted_dict[i][1])



def analyzeCentrality(corporation_network, director_network, all_companies, all_directors):
    print ""
    #Find top 20 most central nodes in corporate network
    print "Most Central Nodes in Corporation-Corporation Network by Network Closeness"
    getCentralNodes(corporation_network, 20, all_companies)
    
    print ""
    #Find top 10 most central nodes in director network
    print "Most Central Nodes in Director-Director Network by Network Closeness"
    getCentralNodes(director_network, 10, all_directors)
    
    
    
def analyzeNodeDegree(corporation_network, director_network, all_companies, all_directors):
    print ""
    #Find top 20 nodes in company network with highest degree
    print "Nodes in Corporation-Corporation Network with Highest Degree"
    getHighestNodeDegrees(corporation_network, 20, all_companies)
    
    print ""
    #Find top 10 nodes in director network with highest degree
    print "Nodes in Director-Director Network with Highest Degree"
    getHighestNodeDegrees(director_network, 10, all_directors)
    

#takes a vector of x,y points and plots them to be used with gnuplot
def printPlotFile(result_vector, file_name):
    print "Printing file %s" % (file_name)
    fo = open(file_name, "w")
    for (x, y) in result_vector:
        fo.write(str(x) + "\t" + str(y) + "\n")
    fo.close()

if __name__ == '__main__': 
    PATHTODATA='./board_relationships.csv'
    
    print "Loading Corporate Network %s" % (PATHTODATA)
    relationships, all_directors, all_companies = parseInputFile(PATHTODATA)
    print "Data Loaded"
    print "Length of all_directors: %d, Length of all_companies: %d" % (len(all_directors), len(all_companies))
    
    director_network, dir_edge_dict = loadDirectorNetwork(relationships, all_directors, all_companies)
    print "Director Network Generated with %d nodes and %d edges" % (director_network.GetNodes(), director_network.GetEdges())
    
    corporation_network, corp_edge_dict = loadCorporationNetwork(relationships, all_directors, all_companies)
    print "Corporation Network Generated with %d nodes and %d edges" % (corporation_network.GetNodes(), corporation_network.GetEdges())

    #WRITE ANALYSIS FUNCITONS AND CALL THEM HERE
    #analyzeCentrality(corporation_network, director_network, all_companies, all_directors)
    #analyzeNodeDegree(corporation_network, director_network, all_companies, all_directors)

    
    
    
    
