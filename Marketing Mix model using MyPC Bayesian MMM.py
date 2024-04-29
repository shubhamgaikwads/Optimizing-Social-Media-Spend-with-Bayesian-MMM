#!/usr/bin/env python
# coding: utf-8

# In[1]:


#! pip install pymc-marketing

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet, SGDRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# In[2]:


import warnings

import arviz as az
import pymc as pm
import seaborn as sns

from pymc_marketing.mmm.delayed_saturated_mmm import DelayedSaturatedMMM
from pymc_marketing.mmm.transformers import geometric_adstock, logistic_saturation


# In[3]:


warnings.filterwarnings("ignore")

az.style.use("arviz-darkgrid")
plt.rcParams["figure.figsize"] = [12, 7]
plt.rcParams["figure.dpi"] = 100

get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('config', 'InlineBackend.figure_format = "retina"')


# In[4]:


# Loading the Dataset
data = pd.read_csv("/Documents/MMM/mmm.csv")


# In[5]:


data.head(10)


# In[6]:


data.drop(columns=["Unnamed: 0"], inplace=True)


# In[7]:


data.info()


# In[8]:


data.describe()


# In[9]:


# Data preprocessing
# Remove irrelevant columns
data.drop(columns=["time.index"], inplace=True)


# In[10]:


data.head(10)


# In[11]:


# Select features and target variable
selected_features = ['tv.spend', 'search.spend', 'revenue']
sale_spend = data[selected_features]


# In[12]:


# Feature Engineering

# Create lag variables for 1y for revenue and channels to look for seasonality
sale_spend = pd.concat([sale_spend, sale_spend.shift(52).add_suffix('_lag1y')], axis=1)
sale_spend['revenue_lag1w'] = sale_spend['revenue'].shift()
sale_spend['revenue_lag3m'] = sale_spend['revenue'].shift(13)


# In[13]:


# Drop extra columns generated from column shift and concatenation
sale_spend = sale_spend.dropna()


# In[14]:


# PyMC MMM Model

with pm.Model() as mmm_model:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta_tv = pm.Normal('beta_tv', mu=0, sigma=1)
    beta_search = pm.Normal('beta_search', mu=0, sigma=1)
    sigma = pm.HalfNormal('sigma', sigma=1)

    # Linear relationship
    mu = alpha + beta_tv * sale_spend['tv.spend'] + beta_search * sale_spend['search.spend']

    # Likelihood
    revenue_obs = pm.Normal('revenue_obs', mu=mu, sigma=sigma, observed=sale_spend['revenue'])


# In[15]:


# Model fitting
with mmm_model:
    trace = pm.sample(1000, tune=1000)


# In[16]:


# Model evaluation
az.plot_trace(trace)
plt.show()


# In[17]:


# Summary statistics
az.summary(trace)


# In[ ]:


# The summary statistics provide information about the posterior distributions of the model parameters. 
# Here's how to interpret the results and understand the impact on revenue:

# alpha: The mean value of alpha is 3.736 with a standard deviation of 0.984. 
# This represents the intercept term in the model. It indicates the baseline revenue 
# when both TV spend and search spend are zero.

# beta_search: The mean value of beta_search is 182.964 with a very small standard deviation of 0.005. 
# This indicates that for every unit increase in search spend, 
# there is an average increase of approximately $182.96 in revenue.

# beta_tv: The mean value of beta_tv is 12.600 with a very small standard deviation of 0.002. 
# This indicates that for every unit increase in TV spend, 
# there is an average increase of approximately $12.60 in revenue.

# sigma: The mean value of sigma is 20208.776, which represents the standard deviation of 
# the error term in the model. This indicates the variability of the observed revenue around 
# the predicted values by the model.


# In[20]:


## Increasing search spend by one unit is estimated to have 
## a much larger impact on revenue compared to increasing TV spend by one unit.

## The standard deviation of the error term (sigma) is relatively large, suggesting that 
## there is still unexplained variability in revenue that is not captured by the model.

## In summary, according to this model, search spend has a larger impact on revenue compared to TV spend. 
## However, it's essential to consider other factors and conduct further analysis to validate 
## these findings and make informed decisions about marketing strategy.

