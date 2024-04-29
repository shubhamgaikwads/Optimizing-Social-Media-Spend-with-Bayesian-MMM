# Marketing-Mix-Modeling-using-PyMC-Bayesian-MMM
This repository demonstrates the use of PyMC-Marketing Bayesian Mix Marketing Model to analyze the impact of the media spend on revenue.

# Introduction:

This repository contains code for building a Marketing Mix Model (MMM) using the PyMC Bayesian approach. MMM is a statistical analysis technique that helps marketers understand the impact of various marketing tactics on sales and revenue. In this project, we use Bayesian methods implemented with PyMC to estimate the effects of TV and search advertising spending on revenue.

# Installation:

You can install the necessary package using pip:

bash
Copy code
pip install pymc-marketing

# Dependencies:

pandas
numpy
scikit-learn
matplotlib
seaborn
arviz
pymc

# Result:


The summary statistics provide information about the posterior distributions of the model parameters. Here's how to interpret the results and understand the impact on revenue:

alpha: The mean value of alpha is 3.736 with a standard deviation of 0.984. This represents the intercept term in the model. It indicates the baseline revenue when both TV spend and search spend are zero.

beta_search: The mean value of beta_search is 182.964 with a very small standard deviation of 0.005. This indicates that for every unit increase in search spend, there is an average increase of approximately $182.96 in revenue.

beta_tv: The mean value of beta_tv is 12.600 with a very small standard deviation of 0.002. This indicates that for every unit increase in TV spend, there is an average increase of approximately $12.60 in revenue.

sigma: The mean value of sigma is 20208.776, which represents the standard deviation of the error term in the model. This indicates the variability of the observed revenue around the predicted values by the model.

# Summary:

The PyMC Bayesian MMM model estimates the effects of TV and search advertising spending on revenue. The summary statistics provide information about the posterior distributions of the model parameters. Based on the analysis, increasing search spend by one unit is estimated to have a much larger impact on revenue compared to increasing TV spend by one unit.

# Contributing:

Contributions to this project are welcome. Feel free to open an issue or submit a pull request.

# Sources:

Data Source: https://github.com/deejayrusso/Marketing-Mix-Model/blob/main/README.md

Model: https://github.com/pymc-labs/pymc-marketing


