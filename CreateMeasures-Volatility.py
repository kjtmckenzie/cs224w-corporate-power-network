
# coding: utf-8

# In[1]:

import pandas as pd

weekly_prices = pd.DataFrame.from_csv('/Users/joshneland/Documents/bigdata/stanford/cs224w_2/project/final_closing_prices.csv')
#weekly_prices = weekly_prices[['AAPL','ABFS']].loc['2000-01-02':'2000-07-23']
weekly_prices


# In[2]:

summaries = pd.rolling_std(weekly_prices.pct_change(periods=1), window=52, min_periods=52)


# In[3]:

df = summaries[summaries.index.isin(['2000-01-02','2001-01-07','2002-01-06','2003-01-12','2004-01-04','2005-01-02','2006-01-08', '2007-01-07',
                                     '2008-01-06','2009-01-04','2010-01-03', '2011-01-02', '2012-01-08','2013-01-06'])]
df = df.transpose()


# In[6]:

df_high_volatility = (df - df.mean()) > 0
df_high_volatility.index.names=['ticker']
df_high_volatility.to_csv('volatility_by_year.csv')


# In[7]:

df_high_volatility


# In[ ]:



