#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

file_enron = './enron-v1.csv'
enron_data = pd.read_csv(file_enron)
enron_data

#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns  # also improves the look of plots
sns.set()  # set Seaborn defaults
plt.rcParams['figure.figsize'] = [10, 5]  # default hor./vert. size of plots, in inches
plt.rcParams['lines.markeredgewidth'] = 1  # to fix issue with seaborn box plots; needed after import seaborn

import plotly.graph_objects as go
import networkx as nx
from pyvis.network import Network
from pyvis import network as net

# Here is my additional stuff
import plotly.express as px
from bokeh.layouts import column, layout, row, Spacer
from bokeh.models import (BasicTicker, ColorBar, ColumnDataSource,
                          LinearColorMapper, PrintfTickFormatter, 
                          Label, ImageURL, RadioGroup, Button, Select,
                          Arrow, NormalHead, LabelSet)
from bokeh.plotting import figure, curdoc
from bokeh.transform import transform, linear_cmap


#// This imports all of the libraries into the programme
import dash
import dash_table
import dash_core_components as dcc
#import dahs_html_components as html
from dash.dependencies import Input, Output

#app = dash.Dash(__name__)
#server = app.server

# In[2]:


enron_data


# In[3]:


first = px.scatter(x= enron_data['date'], y=[enron_data['fromJobtitle']])
first


# In[4]:


sentiment_overview = enron_data['sentiment'].sort_values()
sentiment_overview

enron_data_sorted_by_sentiment = enron_data.sort_values('sentiment')
enron_data_sorted_by_sentiment


# In[5]:


## the entire thing is an interval ranging from -1 to 1


# In[6]:


#Data used for colormapping
mapper = LinearColorMapper(palette="Viridis256", low=sentiment_overview.min(), high=sentiment_overview.max())
mapper


# In[7]:


# I am currently running into trouble with the color mapper.
# I will proceed with red = negative value   / green = positive value / gray = neutral (0)


# In[8]:


enron_data_sorted_by_sentiment['COLOR'] = '.'
for i in range(len(enron_data_sorted_by_sentiment)):
    val= enron_data_sorted_by_sentiment.at[i,'sentiment']
        
    if val > 0 :
        enron_data_sorted_by_sentiment.at[i,'COLOR'] = 'green'
        print('1')
    if val < 0 :
        enron_data_sorted_by_sentiment.at[i,'COLOR'] = 'red'
        print('2') 
    if val == 0 :
        enron_data_sorted_by_sentiment.at[i,'COLOR'] = 'black'
        print('3')


# In[9]:


enron_data_sorted_by_sentiment[enron_data_sorted_by_sentiment['sentiment']== 0]


# In[10]:


colored_graph = px.scatter(x= enron_data_sorted_by_sentiment['date'], 
                           y=  enron_data_sorted_by_sentiment['fromJobtitle'],
                           color = enron_data_sorted_by_sentiment['COLOR'])
colored_graph

# actually it does not use the color I assigned to it. This should be fixed at some point.
# I feel that this is not really useful to be honest.


# In[11]:


director = enron_data_sorted_by_sentiment[enron_data_sorted_by_sentiment['fromJobtitle']== 'Director']
director_sentiment_over_time = px.scatter(x= director['date'], 
                           y=  director['sentiment'],
                           color = director['COLOR'])
director_sentiment_over_time

# This should be automized with the filter we have.


# In[12]:


# The idea is to give an general overview over the categories regarding the sentiment over time.
# We could use this one to interact with other visualizations


# In[16]:


diana = enron_data_sorted_by_sentiment[enron_data_sorted_by_sentiment['fromEmail']== 'diana.scholtes@enron.com']
diana_sentiment_over_time = px.scatter(x= director['date'], 
                           y=  director['sentiment'],
                           color = director['COLOR'])
diana_sentiment_over_time


# In[17]:


# We could also do that with certain persons or an interval of the persons we want. Should be easy using a filter.
# I don't know but to this point I thing a heatmap would be even better since the scatter plot is not really readable.


# In[ ]:




