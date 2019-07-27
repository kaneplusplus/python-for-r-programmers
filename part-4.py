# import math This won't work
import numpy as np
import pandas as pd
import plotnine
from plotnine import *


plotnine.options.figure_size = (2, 1)


wine = pd.read_csv("winemag-data-130k-v2.csv")

wine = wine.drop('Unnamed: 0', axis = 1)

# How many rows?
wine.shape[0]

# How many missing countries?
wine[ ~ wine['country'].isnull() ].shape[0]

# Drop them
wine = wine[ ~ wine['country'].isnull() ]

# What are the column names?
wine.keys()

# How many unique wineries?
len(wine['winery'].unique())

# How many countries?
len(wine['country'].unique())

# Make country categorical, ordered by count.
country_list = wine['country'].value_counts().index.tolist()
country_cat = pd.Categorical(wine['country'], categories = country_list)
wine = wine.assign(country_cat = country_cat)

# Where are the wines from?
(ggplot(wine, aes(x = "country_cat")) +
    theme(axis_text_x=element_text(rotation=270, hjust=1)) +
    geom_histogram())

# How much do they cost?
(ggplot(wine, aes(x = "price")) +
    theme(axis_text_x=element_text(rotation=270, hjust=1)) +
    geom_histogram())

# Let's log. Get rid of NaN's first.
wine = wine[ ~ wine['price'].isna() ]
wine = wine.assign(log_price = np.log(wine['price']))

(ggplot(wine, aes(x = "log_price")) +
    theme(axis_text_x=element_text(rotation=270, hjust=1)) +
    geom_histogram())

# How many types are represented?
variety_count = pd.value_counts(wine.variety.values)

# How many varieties have been rated at least 1000 times?
np.sum(variety_count > 1000)
variety_count = variety_count[variety_count > 1000]

wine = wine[wine.variety.isin(variety_count.keys())]

# What is the average number points per variety?
(wine.points.groupby(wine.variety).describe().sort_values("mean", 
  ascending = False))

# How many tasters?
taster_counts = pd.value_counts(wine['taster_name'].values)

# Let's get the individuals with at least 1000 tastings.
keep_tasters = taster_counts[taster_counts > 1000]

wine = wine[wine.taster_name.isin(keep_tasters.keys())]

(wine.points.groupby(wine.taster_name).describe().sort_values("mean", 
  ascending = False))

# What is the assocation between price and points?
import statsmodels.formula.api as sm

fit = sm.ols(formula = "points ~ price", data = wine).fit()
fit.summary()

# Is there an interaction with variety?
fit = sm.ols(formula = "points ~ log_price + variety", data = wine).fit()
fit = sm.ols(formula = "points ~ log_price + variety + log_price:variety", \
  data = wine).fit()
fit.summary()

# What was the treatment category again?
np.sort(wine.variety.unique())

# Which wine is the most overpriced?
wine = wine.assign(resid = fit.resid)
wine = wine.assign(fitted = fit.fittedvalues)
under_priced = wine[wine.resid == np.max(wine.resid)]
under_priced.keys()
under_priced.values

over_priced = wine[wine.resid == np.min(wine.resid)]
over_priced.values

wine.points.groupby(wine.title).describe().sort_values("mean", ascending = False)
