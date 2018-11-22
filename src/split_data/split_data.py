
# coding: utf-8

# In[1]:


import os
import pandas as pd
pd.options.display.max_rows = None

df=pd.read_csv('../../data/input_output_data.csv')
df1 = df.iloc[:len(df)//6, :]
df2 = df.iloc[len(df)//6:, :]
df1.to_csv('data/data_simulation.csv', index=False)
df2.to_csv('data/data_training.csv', index=False)
