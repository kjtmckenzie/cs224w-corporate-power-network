
# coding: utf-8

# In[45]:

import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model, preprocessing, cross_validation, svm, ensemble


# Is a company's centrality related to its stock's performance?
# Let's calculate the various measures of centrality for each company.

# In[46]:

def load_company_graph(idFilter = lambda x: False):
    graph = nx.Graph()
    with open("corp_edge_dict.csv", "r") as edge_file:
        for line in edge_file:
            
            #Each line has format: "{company id 1} to {company id 2},{number of connections}"
            a, count = line.strip().split(",")
            id1, id2 = a.split(" to ")
            
            id1 = int(id1)
            id2 = int(id2)
            count = float(count)
            
            if not idFilter(id1) and not idFilter(id2):
                graph.add_edge(id1, id2, weight=count)
    
    return graph


# In[47]:

def produce_centrality_measures(G):
    labels = ["centrality_closeness", "centrality_betweenness", "centrality_degree"]
    
    measures = [nx.closeness_centrality(G),
                nx.betweenness_centrality(G),
                nx.degree_centrality(G)]
    
    return pd.DataFrame(measures, index=labels).transpose()


# In[48]:

excludeFilter = lambda x: x > 897
companyGraph = load_company_graph(idFilter=excludeFilter)
centralityMeasures = produce_centrality_measures(companyGraph)


# Then we'll see if these measures correlate with the probability of having above avg performance.

# In[49]:

companyInfo = pd.read_csv("public_company_detail.csv", index_col=0)
companyMeasures = companyInfo.join(centralityMeasures, how='inner')
companyMeasures.index.names=['company_id']


# In[50]:

communityMeasures = pd.read_csv("stationarity_descriptors.csv", index_col=0)
companyMeasures = companyMeasures.join(communityMeasures, how='inner')
companyMeasures


# In[51]:

def normalize_dims(frame, exclude_cols=[]):
    copy = frame.copy()
    
    for c in list(copy.columns.values):
        if c not in exclude_cols:
            print("Normalizing column: {}".format(c))
            copy.loc[:,c] = preprocessing.scale(copy.loc[:,c])
    return copy


# In[52]:

def read_vals(names_to_files_map, summarize_funct):
    finalFrame = None
    for (colname, filename) in names_to_files_map.items():
        df = pd.read_csv(filename, index_col=0)
        result = pd.DataFrame(summarize_funct(df), columns=[colname])
        
        if finalFrame is None:
            finalFrame = result
        else:
            finalFrame = finalFrame.join(result)
            
        finalFrame = finalFrame[pd.notnull(finalFrame[colname])]
    return finalFrame

def binary_above_avg(frame):
    metric = frame.sum(1)
    metric = metric - metric.mean()
    metric[metric > 0] = 1
    metric[metric != 1] = -1
    return metric


targets = read_vals({'good_years': 'above_median_performance_by_year.csv', 'volatile_years': 'volatility_by_year.csv', 'good_decade':'decade_pct_price_change_measure.csv'}, binary_above_avg)

data = pd.merge(companyMeasures, targets, left_on='ticker', right_index=True, how='inner', sort=False)

data = normalize_dims(data, ['name','ticker','sec_cik','num_communities', # Text and stuff 
                             'good_years', 'volatile_years', 'good_decade' # The targets
                             ])  
data.num_communities = (data.num_communities - data.num_communities.mean())/(data.num_communities.max() - data.num_communities.min())
data


# In[59]:

def select_columns_except(frame, exclude=[]):
    cols = list(frame.columns.values)
    for e in exclude:
        print("Removing column: {}".format(e))
        cols.remove(e)
    return frame[cols]

data_X = select_columns_except(data, exclude=['name','ticker','sec_cik', 'good_years', 'volatile_years', 'good_decade',
                                              'centrality_closeness',
                                              'centrality_betweenness', 
                                              'centrality_degree', 
                                              #'num_communities',
                                              #'max_intensity', 
                                              'min_stationarity', 
                                              'max_stationarity',
                                              'ave_stationarity', 
                                              #'volatility_of_max_intensity'
                                              ])


# In[60]:

def run_tests(models, X, targetsAndLabels):
    with open('testResults.csv', 'w') as f:
        for model in models:
            #print("Trying model {}".format(model))

            for (label, targetVals) in targetsAndLabels.items():
                scores = cross_validation.cross_val_score(model, X, targetVals.values, cv=10)            
                randVals = targetVals.reindex(np.random.permutation(targetVals.index)).values
                scoresRand = cross_validation.cross_val_score(model, X, randVals, cv=10)
                f.write("\"%s\",\"%s\",%0.2f,%0.2f,%0.2f,%0.2f\n" % (model, label, scores.mean(), scores.std() * 2, scoresRand.mean(), scoresRand.std()*2))

                #print(np.matrix([targetVals.values, randVals]))


models = [linear_model.LogisticRegression(C=0.5), ensemble.RandomForestClassifier(n_estimators=10), svm.SVC(), svm.SVC(kernel="linear"), svm.SVC(kernel="poly")]

run_tests(models, data_X, {'good_year': data.good_years,'volatile_year': data.volatile_years, 'good_decade': data.good_decade})

# Model, target_dim, features: performance / random performance


# In[54]:




# In[73]:

predictions = model.predict(data_X_test)


# In[43]:

results = pd.DataFrame(data_y_test)
results['prediction'] = predictions
results.to_csv('testing_results.csv')


# In[ ]:



