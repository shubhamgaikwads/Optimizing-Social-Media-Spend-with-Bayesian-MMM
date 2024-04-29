#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install pymc arviz


# In[2]:


import pymc as pm
import arviz as az
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[7]:


data = pd.DataFrame({
    'Instagram': np.random.uniform(50, 200, 100),
    'Facebook': np.random.uniform(50, 200, 100),
    'Twitter': np.random.uniform(50, 200, 100),
    'TikTok': np.random.uniform(50, 200, 100),
    'ContentType': np.random.choice(['Video', 'Image', 'Text'], 100),
    'TargetGroup': np.random.choice(['Teen', 'Adult', 'Senior'], 100),
    'Sales': np.random.uniform(100, 500, 100),
})


# In[8]:


data.head(10)


# In[9]:


data.info()


# In[10]:


with pm.Model() as marketing_mix_model:
    beta_instagram = pm.Normal("beta_instagram", mu=0, sigma=10)
    beta_facebook = pm.Normal("beta_facebook", mu=0, sigma=10)
    beta_twitter = pm.Normal("beta_twitter", mu=0, sigma=10)
    beta_tiktok = pm.Normal("beta_tiktok", mu=0, sigma=10)
    
    intercept = pm.Normal("intercept", mu=0, sigma=10)
    sigma = pm.HalfNormal("sigma", sigma=10)
    
    # Linear model to predict sales based on marketing spend
    mu = (
        intercept +
        beta_instagram * data['Instagram'] +
        beta_facebook * data['Facebook'] +
        beta_twitter * data['Twitter'] +
        beta_tiktok * data['TikTok']
    )
    
    # Likelihood for observed data
    sales = pm.Normal("sales", mu=mu, sigma=sigma, observed=data['Sales'])
    
    # Sample the posterior
    trace = pm.sample(2000, tune=1000, cores=1, return_inferencedata=True)


# In[ ]:


#!pip install fastapi uvicorn


# In[11]:


# Function to calculate optimal marketing spend based on Bayesian coefficients
def calculate_optimal_spend(trace, budget, content_type, target_group):
    # Extract posterior means for each coefficient
    beta_instagram = np.mean(az.extract_dataset(trace)["beta_instagram"])
    beta_facebook = np.mean(az.extract_dataset(trace)["beta_facebook"])
    beta_twitter = np.mean(az.extract_dataset(trace)["beta_twitter"])
    beta_tiktok = np.mean(az.extract_dataset(trace)["beta_tiktok"])

    # Calculate initial proportions for each channel
    total_coeff = beta_instagram + beta_facebook + beta_twitter + beta_tiktok
    instagram_proportion = beta_instagram / total_coeff
    facebook_proportion = beta_facebook / total_coeff
    twitter_proportion = beta_twitter / total_coeff
    tiktok_proportion = beta_tiktok / total_coeff
    
    # Default optimal spend based on budget and proportions
    optimal_spend = {
        "Instagram": budget * instagram_proportion,
        "Facebook": budget * facebook_proportion,
        "Twitter": budget * twitter_proportion,
        "TikTok": budget * tiktok_proportion,
    }

    # Adjustments based on content type
    if content_type == 'Video':
        # Favor channels known for video content
        optimal_spend["Instagram"] *= 1.2
        optimal_spend["TikTok"] *= 1.2

    if content_type == 'Image':
        # Favor Instagram and Facebook for image-based content
        optimal_spend["Instagram"] *= 1.1
        optimal_spend["Facebook"] *= 1.1

    if content_type == 'Text':
        # Favor Facebook and Twitter for text-based content
        optimal_spend["Facebook"] *= 1.1
        optimal_spend["Twitter"] *= 1.1

    # Adjustments based on target group
    if target_group == 'Teen':
        optimal_spend["Instagram"] *= 1.1
        optimal_spend["TikTok"] *= 1.2

    if target_group == 'Adult':
        optimal_spend["Facebook"] *= 1.1
        optimal_spend["Twitter"] *= 1.1

    if target_group == 'Senior':
        optimal_spend["Facebook"] *= 1.2
        optimal_spend["Twitter"] *= 1.2
    
    # Normalize to ensure budget constraint
    total_spend = sum(optimal_spend.values())
    if total_spend > budget:
        adjustment_factor = budget / total_spend
        for channel in optimal_spend:
            optimal_spend[channel] *= adjustment_factor
    
    return optimal_spend


# In[12]:


# Example input: given budget, content type, and target group
total_budget = 1000
content_type = "Video"
target_group = "Teen"

# Calculate optimal spend with updated marketing channels and given budget, content type, and target group
optimal_spend = calculate_optimal_spend(trace, total_budget, content_type, target_group)

# Display the optimal spend for each marketing channel
print("Optimal marketing spend allocation:")
for channel, spend in optimal_spend.items():
    print(f"{channel}: ${spend:.2f}")


# In[ ]:




