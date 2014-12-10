
# coding: utf-8

# In[1]:

import pandas as pd

weekly_prices = pd.DataFrame.from_csv('/Users/joshneland/Documents/bigdata/stanford/cs224w_2/project/final_closing_prices.csv')
weekly_prices


# In[6]:

price_change = (weekly_prices.loc['2013-01-06'] - weekly_prices.loc['2000-01-02'])/weekly_prices.loc['2000-01-02']
pd.DataFrame(price_change, columns=['pct_price_change']).to_csv('decade_pct_price_change_measure.csv')


# In[6]:




# In[ ]:



