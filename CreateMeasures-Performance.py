
# coding: utf-8

# In[1]:

import pandas as pd

weekly_prices = pd.DataFrame.from_csv('/Users/joshneland/Documents/bigdata/stanford/cs224w_2/project/final_closing_prices.csv')
weekly_prices


# In[3]:

#summaries = pd.rolling_mean(weekly_prices.pct_change(periods=1), window=52, min_periods=52)
summaries = weekly_prices.pct_change(periods=52)
summaries


# In[4]:

df = summaries[summaries.index.isin(['2000-01-02','2001-01-07','2002-01-06','2003-01-12','2004-01-04','2005-01-02','2006-01-08', '2007-01-07',
                                     '2008-01-06','2009-01-04','2010-01-03', '2011-01-02', '2012-01-08','2013-01-06'])]
df


# In[8]:

df = df.transpose()
df.median()


# In[11]:

df_better_than_avg = (df - df.mean()) > 0
df_better_than_avg.index.names=['ticker']
df_better_than_avg.to_csv('above_mean_performance_by_year.csv')


# In[12]:

df_better_than_avg


# In[ ]:



