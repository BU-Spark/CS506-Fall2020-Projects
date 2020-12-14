#!/usr/bin/env python
# coding: utf-8

# In[595]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import fetch_20newsgroups
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.datasets import make_blobs
from sklearn.mixture import GaussianMixture
from sklearn import linear_model
from sklearn.linear_model import TweedieRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler


from math import sqrt

import math

import folium

get_ipython().run_line_magic('matplotlib', 'inline')


# In[596]:


import statsmodels.api as sm
import statsmodels.formula.api as smf

from itertools import groupby
from operator import itemgetter

from mpl_toolkits.mplot3d import Axes3D

import mlxtend

from mlxtend.preprocessing import minmax_scaling


# In[3]:


parse_dates = ['date']

covid_tigeryi = pd.read_csv("covid_tigeryi.csv", parse_dates=parse_dates, index_col=False)

covid_tigeryi.head()


# In[4]:


demographic_tigeryi = pd.read_csv("demographic_tigeryi.csv", index_col=False)

demographic_tigeryi.head()


# In[5]:


election_tigeryi = pd.read_csv("election_tigeryi.csv", index_col=False)

election_tigeryi.head()


# In[6]:


poll_tigeryi = pd.read_csv("poll_tigeryi.csv", index_col=False, parse_dates=parse_dates)

poll_tigeryi.head()


# In[915]:


def poll_state(poll_tigeryi, state="Florida", usa_state_code=None):
    if state in poll_tigeryi['state'].tolist():
        poll_state = poll_tigeryi[poll_tigeryi['state']==state]
    elif usa_state_code in poll_tigeryi['usa_state_code'].tolist():
        poll_state = poll_tigeryi[poll_tigeryi['usa_state_code']==usa_state_code]
    else:
        raise ValueError("state not valid")
        
    actual_result = poll_state['dem_2020_margin'].tolist()[0]
    actual_result = np.round(actual_result, 3)
    
    poll_average = np.mean(poll_state["dem_lead"])
    poll_average = np.round(poll_average, 3)
    
    last_month_avg = np.mean(poll_state["dem_lead"][-31:-1])
    last_month_avg = np.round(last_month_avg, 3)
    
    error_average = np.mean(poll_state["dem_lead_result_poll_diff"])
    error_average = np.round(error_average, 3)
    
    last_month_error = np.mean(poll_state["dem_lead_result_poll_diff"][-31:-1])
    last_month_error = np.round(last_month_error, 3)
    
    plt.subplots(figsize = (15,5))
    
    plt.subplot(1,2,1)
    
    plt.plot(poll_state["date"], [poll_average]*len(poll_state["date"]), "green", label=f"overall polls avg {poll_average}%")
    plt.plot(poll_state["date"], [last_month_avg]*len(poll_state["date"]), "purple", label=f"last month polls avg {last_month_avg}%")
    plt.plot(poll_state["date"], poll_state["dem_lead"], "-" , label="national polls daily") # 
    plt.plot(poll_state["date"], poll_state["dem_2020_margin"], "r-", label=f"actual election result {actual_result}%")
    plt.legend(loc="lower right")
    plt.xlabel("Date")
    plt.xticks(rotation = 25)
    plt.ylabel("DEM Lead or Deficit vs. REP (%)")
    
    plt.title(f"National Polls Margin DEM - REP in {state or usa_state_code}")  
    
    
    plt.subplot(1,2,2)
    
    plt.title(f"Polls Error for DEM Lead in {state or usa_state_code}")
    
    plt.plot(poll_state["date"], poll_state["dem_lead_result_poll_diff"], "-" , label="national polls error")
    plt.xlabel("Date")
    plt.xticks(rotation = 25)
    plt.ylabel("Polls Error: DEM Lead Margin - Elction Result (%)")
    plt.plot(poll_state["date"], [0]*len(poll_state["date"]), "red", label="no error perfect poll 0%")
    
    plt.plot(poll_state["date"], [error_average]*len(poll_state["date"]), "green", label=f"overall polls error avg {error_average}%")
    plt.plot(poll_state["date"], [last_month_error]*len(poll_state["date"]), "purple", label=f"last month polls error avg {last_month_error}%")

    
    plt.legend(loc="upper right")
    
    
    #return poll_state
    


# In[916]:


poll_state(poll_tigeryi, "Georgia")
poll_state(poll_tigeryi, "Florida")




# In[10]:


poll_state(poll_tigeryi, "North Carolina")
poll_state(poll_tigeryi, "Arizona")


# In[11]:


poll_state(poll_tigeryi, "Pennsylvania")
poll_state(poll_tigeryi, "Wisconsin")



# In[12]:


poll_state(poll_tigeryi, "Michigan")
poll_state(poll_tigeryi, "Nevada")


# In[346]:


# df222 = poll_tigeryi[poll_tigeryi['state']=='Wisconsin']#.loc['2020-06-01':]
# df222 = df222.set_index(['date'])
# df222.loc['2020-6-1':'2020-11-03']
# mask = (df222['date'] >= '2020-03-01') & (df222['date'] <= '2020-11-03')
# df222.loc[mask]
# df222["dem_lead"][-3:-1]


# In[354]:


poll_covid = pd.merge(poll_tigeryi, covid_tigeryi, how = 'inner',
                      left_on = ['state', 'date','usa_state_code'], right_on = ['state', 'date','state_code']
                     )


# In[359]:


poll_covid = poll_covid.dropna(subset=['death_delta','death'], axis=0)



# In[366]:


# poll_covid = poll_covid.drop(5197,axis=0)


# In[388]:


poll_covid['positive_delta_rolling7'] = poll_covid['positive_delta'].rolling(7, min_periods = 0).mean()
poll_covid['negative_delta_rolling7'] = poll_covid['negative_delta'].rolling(7, min_periods = 0).mean()
poll_covid['totalTestResults_delta_rolling7'] = poll_covid['totalTestResults_delta'].rolling(7, min_periods = 0).mean()
poll_covid['death_delta_rolling7'] = poll_covid['death_delta'].rolling(7, min_periods = 0).mean()

poll_covid['positive_rate_delta_rolling7'] = 100* poll_covid['positive_delta_rolling7']/poll_covid['totalTestResults_delta_rolling7']

poll_covid = poll_covid.replace(np.inf, np.nan)


# In[398]:


mask = (poll_covid['positive_rate_delta_rolling7'] >= 0) & (poll_covid['positive_rate_delta_rolling7'] <= 100)
poll_covid = poll_covid.loc[mask]


# In[400]:


poll_covid.to_csv('poll_covid_tigeryi.csv', index=False)


# In[13]:


poll_covid = pd.read_csv('poll_covid_tigeryi.csv', parse_dates=parse_dates, index_col=False)


# In[14]:


# poll_covid_nevada = poll_covid[poll_covid['state']=='Nevada']


# In[195]:


def poll_cov(poll, state="Florida", usa_state_code=None):
    if state in poll['state'].tolist():
        poll_state = poll[poll['state']==state]
    elif usa_state_code in poll['usa_state_code'].tolist():
        poll_state = poll[poll['usa_state_code']==usa_state_code]
    else:
        raise ValueError("state not valid")
        
        
        
        
    actual_result = poll_state['dem_2020_margin'].tolist()[0]
    actual_result = np.round(actual_result, 3)
    
    poll_average = np.mean(poll_state["dem_lead_rolling_7"])
    poll_average = np.round(poll_average, 3)
    
    last_month_avg = np.mean(poll_state["dem_lead_rolling_7"][-31:-1])
    last_month_avg = np.round(last_month_avg, 3)
    
    error_average = np.mean(poll_state["dem_lead_rolling_7_diff"])
    error_average = np.round(error_average, 3)
    
    last_month_error = np.mean(poll_state["dem_lead_rolling_7_diff"][-31:-1])
    last_month_error = np.round(last_month_error, 3)
    
    
    plt.subplots(figsize = (20,20))
    
    plt.subplot(2,3,1)
    
    plt.plot(poll_state['date'],poll_state['positive_rate_delta_rolling7']) # positive_rate_delta_rolling7
    plt.legend(loc="lower right")
    plt.xlabel("Date")
    plt.xticks(rotation = 25)
    plt.ylabel("Covid-19 Positive Rate 7 day rolling (%)")
    
    plt.title(f"Covid-19 Positive Rate (7 day rolling) in {state or usa_state_code}")  
    
    
    plt.subplot(2,3,2)
    
    plt.title(f"National Polls Margin DEM - REP (7 day rolling) in {state or usa_state_code}")
    plt.plot(poll_state['date'], poll_state['dem_lead_rolling_7'], label="national polls DEM margin") 
    
    
    # add here
    plt.plot(poll_state["date"], [poll_average]*len(poll_state["date"]), "green", label=f"overall polls avg {poll_average}%")
    plt.plot(poll_state["date"], [last_month_avg]*len(poll_state["date"]), "purple", label=f"last month polls avg {last_month_avg}%")
    plt.plot(poll_state["date"], poll_state["dem_2020_margin"], "r-", label=f"actual election result {actual_result}%")
    
    
    
    plt.xlabel("Date")
    plt.xticks(rotation = 25)
    plt.ylabel("Nation Polls DEM Lead or Deficit vs. REP 7 day rolling (%)")
        
    plt.legend(loc="lower right")
    
    
    plt.subplot(2,3,3)
    
    
    plt.title(f"Polls Error of DEM Lead (7 day rolling) in {state or usa_state_code}")
    
    plt.plot(poll_state["date"], poll_state["dem_lead_rolling_7_diff"], "-" , label="national polls error")
    plt.xlabel("Date")
    plt.xticks(rotation = 25)
    plt.ylabel("Polls Error: DEM Lead Margin - Elction Result 7 day rolling (%)")
    
    # add here
    plt.plot(poll_state["date"], [0]*len(poll_state["date"]), "red", label="no error perfect poll 0%")
    plt.plot(poll_state["date"], [error_average]*len(poll_state["date"]), "green", label=f"overall polls error avg {error_average}%")
    plt.plot(poll_state["date"], [last_month_error]*len(poll_state["date"]), "purple", label=f"last month polls error avg {last_month_error}%")


    
        
    plt.legend(loc="lower right")
    
    
    
    plt.subplot(2,3,4)
    
    plt.title(f"Polls DEM - REP VS. Covid-19 Positive Rate in {state or usa_state_code}")
    
    X1 = poll_state['positive_rate_delta_rolling7']
    Y1 = poll_state['dem_lead_rolling_7']
    
    plt.scatter(X1, Y1, alpha=0.2, label='Poll DEM Lead')

    results = sm.WLS(Y1, sm.add_constant(X1), weights=list(range(0,len(X1)))).fit() # OLS
    X_plot = np.linspace(0, 20, 101)
    a1 = results.params[1]
    b1 = results.params[0]
    Y_plot = X_plot*a1 + b1
    plt.plot(X_plot, Y_plot, 'r-', label=f"y = {np.round(a1,2)}*x + {np.round(b1,2)}", alpha=0.8)
    plt.legend(loc="lower right")
    plt.xlabel("Covid daily postive rate (rolling 7 day average) %")
    plt.ylabel("Nation Polls DEM Lead or Deficit vs. REP 7 day rolling (%)")
             
    #print(results.params)
    #print(results.summary())
    print()
    
    
    
 
    plt.subplot(2,3,5)
    
    plt.title(f"Polls Error VS. Covid-19 Positive Rate in {state or usa_state_code}")
    
    X2 = poll_state['positive_rate_delta_rolling7']
    Y2 = poll_state['dem_lead_rolling_7_diff']
    plt.scatter(X2, Y2, alpha=0.2, label='polling error')

    results2 = sm.WLS(Y2, sm.add_constant(X2), weights=list(range(0,len(X2)))).fit()
    X_plot = np.linspace(0, 20, 101)
    a2 = results2.params[1]
    b2 = results2.params[0]
    Y_plot = X_plot*a2 + b2
    plt.plot(X_plot, Y_plot, 'r-', label=f"y = {np.round(a2,2)}*x + {np.round(b2,2)}", alpha=0.8)
    plt.legend(loc="upper right")
    plt.xlabel("Covid daily postive rate (rolling 7 day average) %")
    plt.ylabel("Polls Error: DEM Lead Margin - Elction Result 7 day rolling (%)")
    
    #print(results2.params)
    print(results2.summary())
    
        


# In[196]:



poll_cov(poll_covid, "Florida")


# In[197]:


poll_cov(poll_covid, "Ohio")


# In[198]:


poll_cov(poll_covid, "Nevada")


# In[199]:


poll_cov(poll_covid, "North Carolina")



# In[200]:


poll_cov(poll_covid, "Georgia")



# In[201]:


poll_cov(poll_covid, "Pennsylvania")



# In[202]:


poll_cov(poll_covid, "Wisconsin")



# In[145]:


poll_covid_election_day = poll_covid[poll_covid['date']=='2020-11-03']


# In[147]:


poll_covid_election_day.head()


# In[233]:


covid_positive_election_day = poll_covid_election_day['positive_rate_delta_rolling7'].tolist()

poll_dem_margin = poll_covid_election_day['dem_lead_rolling_7'].tolist()

poll_error_election_day = poll_covid_election_day['dem_lead_rolling_7_diff'].tolist()

states_election_day = poll_covid_election_day['state_code'].tolist()

result_election_day = poll_covid_election_day['dem_2020_margin'].tolist()

# margin_shift = poll_covid_election_day['margin_shift'].tolist()


# In[220]:


battleground_states = ['Florida', 'Georgia', 'Arizona', 
                       'Wisconsin', 'Pennsylvania', 'Nevada',
                       'Michigan', 'Minnesota', 'North Carolina',
                       'Texas', 'Ohio', 'Iowa'
                      ]

poll_covid_election_battleground = poll_covid_election_day.loc[poll_covid_election_day['state'].isin(battleground_states)]

poll_covid_election_battleground.head()


# In[221]:


covid_positive_election_day_battleground = poll_covid_election_battleground['positive_rate_delta_rolling7'].tolist()

poll_dem_margin_battleground = poll_covid_election_battleground['dem_lead_rolling_7'].tolist()

poll_error_election_day_battleground = poll_covid_election_battleground['dem_lead_rolling_7_diff'].tolist()

states_election_day_battleground = poll_covid_election_battleground['state_code'].tolist()

result_election_day_battleground = poll_covid_election_battleground['dem_2020_margin'].tolist()




# In[218]:



# plt.scatter(covid_positive_election_day, poll_dem_margin, alpha=0.5)

fig, ax = plt.subplots(figsize = (20,10))

ax.scatter(covid_positive_election_day, poll_dem_margin, alpha=0.5)

for i, txt in enumerate(states_election_day):
    ax.annotate(txt, (covid_positive_election_day[i], poll_dem_margin[i]), alpha =0.7)


results = sm.OLS(poll_dem_margin, sm.add_constant(covid_positive_election_day)).fit()

X_plot = np.linspace(0, 50, 501)
a = results.params[1]
b = results.params[0]
Y_plot = X_plot*a + b
Y_flat = [0]*len(X_plot)

plt.plot(X_plot, Y_plot, 'r-', label=f"y = {np.round(a,2)}*x + {np.round(b,2)}", alpha=0.8)
plt.plot(X_plot, Y_flat, 'b-', label="DEM tie with REP in Polls", alpha=0.6)


plt.legend(loc="upper right")
plt.xlabel("Covid daily postive rate on Election Day (rolling 7 day avg) %")
plt.ylabel("Polls DEM Lead: DEM - REP (7 day rolling avg) (%)")
plt.title("Election day 2020-11-03 Poll DEM Lead (DEM - REP) vs. Covid-19 Positive Rate (7 day rolling avg)")
    
plt.show()

print(results.params)
print(results.summary())


# In[223]:



# plt.scatter(covid_positive_election_day, dem_2020_margin, alpha=0.5)

# result_election_day

fig, ax = plt.subplots(figsize = (20,10))

ax.scatter(covid_positive_election_day, result_election_day, alpha=0.5)

for i, txt in enumerate(states_election_day):
    ax.annotate(txt, (covid_positive_election_day[i], result_election_day[i]), alpha =0.7)


results = sm.OLS(result_election_day, sm.add_constant(covid_positive_election_day)).fit()

X_plot = np.linspace(0, 50, 501)
a = results.params[1]
b = results.params[0]
Y_plot = X_plot*a + b
Y_flat = [0]*len(X_plot)

plt.plot(X_plot, Y_plot, 'r-', label=f"y = {np.round(a,2)}*x + {np.round(b,2)}", alpha=0.8)
plt.plot(X_plot, Y_flat, 'b-', label="DEM tie with REP in Election Result", alpha=0.6)


plt.legend(loc="upper right")
plt.xlabel("Covid daily postive rate on Election Day (rolling 7 day avg) %")
plt.ylabel("Election Result of DEM Lead (DEM - REP) (7 day rolling avg) (%)")
plt.title("2020-11-03 Election Final Result: DEM Lead (DEM - REP) vs. Covid-19 Positive Rate (7 day rolling avg)")
    
plt.show()

print(results.params)
print(results.summary())



# In[214]:


fig, ax = plt.subplots(figsize = (20,10))

ax.scatter(covid_positive_election_day, poll_error_election_day, alpha=0.5)

for i, txt in enumerate(states_election_day):
    ax.annotate(txt, (covid_positive_election_day[i], poll_error_election_day[i]), alpha =0.7)


results2 = sm.OLS(poll_error_election_day, sm.add_constant(covid_positive_election_day)).fit()

X_plot = np.linspace(0, 50, 501)
a2 = results2.params[1]
b2 = results2.params[0]
Y_plot = X_plot*a2 + b2
Y_flat = [0]*len(X_plot)

plt.plot(X_plot, Y_plot, 'r-', label=f"y = {np.round(a2,2)}*x + {np.round(b2,2)}", alpha=0.8)
plt.plot(X_plot, Y_flat, 'b-', label="Perfect Poll on Election Result", alpha=0.6)


plt.legend(loc="upper right")
plt.xlabel("Covid daily postive rate on Election Day (rolling 7 day avg) %")
plt.ylabel("Polls Error: DEM Poll Lead - Elction Result (7 day rolling avg) (%)")
plt.title("Election day 2020-11-03 Poll Error (DEM Result - Poll) vs. Covid-19 Positive Rate (7 day rolling avg)")
    
plt.show()

print(results2.params)
print(results2.summary())


# In[224]:


covid_positive_election_day_battleground = poll_covid_election_battleground['positive_rate_delta_rolling7'].tolist()

poll_dem_margin_battleground = poll_covid_election_battleground['dem_lead_rolling_7'].tolist()

poll_error_election_day_battleground = poll_covid_election_battleground['dem_lead_rolling_7_diff'].tolist()

states_election_day_battleground = poll_covid_election_battleground['state_code'].tolist()

result_election_day_battleground = poll_covid_election_battleground['dem_2020_margin'].tolist()


# In[229]:


# plt.scatter(covid_positive_election_day_battleground, poll_dem_margin_battleground, alpha=0.5)

fig, ax = plt.subplots(figsize = (10,5))

ax.scatter(covid_positive_election_day_battleground, poll_dem_margin_battleground, alpha=0.5)

for i, txt in enumerate(states_election_day_battleground):
    ax.annotate(txt, (covid_positive_election_day_battleground[i], poll_dem_margin_battleground[i]), alpha =0.7)


results = sm.OLS(poll_dem_margin_battleground, sm.add_constant(covid_positive_election_day_battleground)).fit()

X_plot = np.linspace(0, 50, 501)
a = results.params[1]
b = results.params[0]
Y_plot = X_plot*a + b
Y_flat = [0]*len(X_plot)

plt.plot(X_plot, Y_plot, 'r-', label=f"y = {np.round(a,2)}*x + {np.round(b,2)}", alpha=0.8)
plt.plot(X_plot, Y_flat, 'b-', label="DEM tie with REP in Polls", alpha=0.6)


plt.legend(loc="upper right")
plt.xlabel("Covid daily postive rate on Election Day (rolling 7 day avg) %")
plt.ylabel("Polls DEM Lead: DEM - REP (7 day rolling avg) (%)")
plt.title("Election day 2020-11-03 Poll DEM Lead (DEM - REP) vs. Covid-19 Positive Rate (7 day rolling avg)")
    
plt.show()

print(results.params)
print(results.summary())



# In[230]:



# plt.scatter(covid_positive_election_day_battleground, result_election_day_battleground, alpha=0.5)

# result_election_day

fig, ax = plt.subplots(figsize = (10,5))

ax.scatter(covid_positive_election_day_battleground, result_election_day_battleground, alpha=0.5)

for i, txt in enumerate(states_election_day_battleground):
    ax.annotate(txt, (covid_positive_election_day_battleground[i], result_election_day_battleground[i]), alpha =0.7)


results = sm.OLS(result_election_day_battleground, sm.add_constant(covid_positive_election_day_battleground)).fit()

X_plot = np.linspace(0, 50, 501)
a = results.params[1]
b = results.params[0]
Y_plot = X_plot*a + b
Y_flat = [0]*len(X_plot)

plt.plot(X_plot, Y_plot, 'r-', label=f"y = {np.round(a,2)}*x + {np.round(b,2)}", alpha=0.8)
plt.plot(X_plot, Y_flat, 'b-', label="DEM tie with REP in Election Result", alpha=0.6)


plt.legend(loc="upper right")
plt.xlabel("Covid daily postive rate on Election Day (rolling 7 day avg) %")
plt.ylabel("Election Result of DEM Lead (DEM - REP) (7 day rolling avg) (%)")
plt.title("2020-11-03 Election Final Result: DEM Lead (DEM - REP) vs. Covid-19 Positive Rate (7 day rolling avg)")
    
plt.show()

print(results.params)
print(results.summary())




# In[231]:


fig, ax = plt.subplots(figsize = (10,5))

ax.scatter(covid_positive_election_day_battleground, poll_error_election_day_battleground, alpha=0.5)

for i, txt in enumerate(states_election_day_battleground):
    ax.annotate(txt, (covid_positive_election_day_battleground[i], poll_error_election_day_battleground[i]), alpha =0.7)


results2 = sm.OLS(poll_error_election_day_battleground, sm.add_constant(covid_positive_election_day_battleground)).fit()

X_plot = np.linspace(0, 50, 501)
a2 = results2.params[1]
b2 = results2.params[0]
Y_plot = X_plot*a2 + b2
Y_flat = [0]*len(X_plot)

plt.plot(X_plot, Y_plot, 'r-', label=f"y = {np.round(a2,2)}*x + {np.round(b2,2)}", alpha=0.8)
plt.plot(X_plot, Y_flat, 'b-', label="Perfect Poll on Election Result", alpha=0.6)


plt.legend(loc="upper right")
plt.xlabel("Covid daily postive rate on Election Day (rolling 7 day avg) %")
plt.ylabel("Polls Error: DEM Poll Lead - Elction Result (7 day rolling avg) (%)")
plt.title("Election day 2020-11-03 Poll Error (DEM Result - Poll) vs. Covid-19 Positive Rate (7 day rolling avg)")
    
plt.show()

print(results2.params)
print(results2.summary())


# In[789]:


demographic_tigeryi.head()


# In[238]:



scaler = MinMaxScaler()


# In[796]:


vars_to_merge = [x for x in demographic_tigeryi.columns if x not in ['state', 'county','state_code']]

df = pd.DataFrame(demographic_tigeryi.groupby(['state', 'county'])[vars_to_merge].sum())

df.head(5)


# In[797]:


df = df.drop(['dem_16_margin', 'dem_20_margin', 'dem_margin_shift'], axis=1)
df.head()


# In[798]:


df = df.drop(['lat', 'long'], axis=1)

df.head()


# In[799]:


df = df.drop(["Men", "Women", "VotingAgeCitizen", "Employed",
 "Income","IncomeErr","IncomePerCap", "IncomePerCapErr",
 "cases", "deaths", "TotalPop", "VotingAgeCitizen", "Employed"], axis=1)
df.head()


# In[800]:


df.to_csv("df_tigeryi.csv", index=False)


# In[605]:


# df = pd.read_csv("df_tigeryi.csv", index_col=False)


# In[801]:


df.head()


# In[802]:


# min max scaling
df_final = minmax_scaling(df, columns=df.columns)
df_final.head()


# In[803]:


votes_perc = df[['percentage20_Donald_Trump', 'percentage20_Joe_Biden', 
                 'votes20_Donald_Trump', 'votes20_Joe_Biden']].columns


# In[804]:


PearsonCorr = df_final.corr(method="pearson")


# In[805]:


Pearson = PearsonCorr[votes_perc]


# In[806]:


SpearmanCorr = df_final.corr(method="spearman")


# In[807]:


Spear = SpearmanCorr[votes_perc]


# In[808]:


# Correlation Diagram

plt.subplots(figsize = (20,20))
    
plt.subplot(1,2,1)

plt.title("SpearmanCorr")

ax1 = sns.heatmap(Spear, vmax=.9, square=True, annot=True, linewidths=.3, cmap="YlGnBu", fmt='.1f') 

plt.subplot(1,2,2)

plt.title("PearsonCorr")

ax2 = sns.heatmap(Pearson, vmax=.9, square=True, annot=True, linewidths=.3, cmap="YlGnBu", fmt='.1f') 

plt.show()


# In[809]:


votes = df_final.iloc[:,0:10].columns
votes


# In[810]:


factors =  [x for x in df.columns if x not in votes]



# In[811]:


# GM clustering

X = df_final[factors].values

GM_n_components = np.arange(1, 15)
GM_models = [GaussianMixture(n, covariance_type='full', random_state=0).fit(X) for n in GM_n_components]

plt.figure(num=None, figsize=(8, 6), dpi=60, facecolor='w', edgecolor='r')
plt.plot(GM_n_components, [m.aic(X) for m in GM_models], label='AIC')
plt.tight_layout()
plt.legend(loc='best')
plt.xlabel('n_components')


# In[812]:


# GM clustering - Gaussian Mixture Model

GM_n_classes = 2

GMcluster = GaussianMixture(n_components=GM_n_classes, covariance_type='full',random_state = 0)

GMcluster_fit = GMcluster.fit(df_final)

GMlabels = GMcluster_fit.predict(df_final)

print('Number of clusters: ' + format(len(np.unique(GMlabels))))


# In[813]:


unique, counts = np.unique(GMlabels, return_counts=True)
dict(zip(unique, counts))


# In[822]:


# GM clustering - Gaussian Mixture Model

fig = plt.figure(figsize=(8, 6),facecolor='w', edgecolor='r')
ax = Axes3D(fig, rect = (1, 1, 1, 1))
ax.set_xlim3d(0, 1)
ax.set_ylim3d(0, 1)
ax.set_zlim3d(0, 1)
ax.view_init(10, 40)
for l in np.unique(GMlabels):
    ax.scatter(X[GMlabels == l, 0], X[GMlabels == l, 1], X[GMlabels == l, 2],
               color=plt.cm.jet(float(l) / np.max(GMlabels + 1)),s=20, edgecolor='k')
plt.title('Gaussian Mixture Model clustering' )

plt.show()


# In[823]:


df_final['Party_Cluster'] = GMlabels


# In[824]:


pca = PCA().fit(df_final)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5), dpi=70, facecolor='w', edgecolor='k')
ax0, ax1 = axes.flatten()

sns.set('talk', palette='colorblind')

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}

matplotlib.rc('font', **font)

ax0.plot(np.cumsum(pca.explained_variance_ratio_), marker='.')
ax0.set_xlabel('Number of components')
ax0.set_ylabel('Cumulative explained variance');

ax1.bar(range(df_final.shape[1]),pca.explained_variance_)
ax1.set_xlabel('Number of components')
ax1.set_ylabel('Explained variance');

plt.tight_layout()
plt.show()


# In[825]:


n_PCA_90 = np.size(np.cumsum(pca.explained_variance_ratio_)>0.9) - np.count_nonzero(np.cumsum(pca.explained_variance_ratio_)>0.9)

print("Need: " + format(n_PCA_90) + " components to cover 90% of variance.")



# In[826]:


pca = PCA(11).fit(df_final)

X_pca=pca.transform(df_final) 

plt.matshow(pca.components_,cmap='viridis')
plt.yticks([0,1,2,3,4,5],['1st Comp','2nd Comp','3rd Comp','4th Comp','5th Comp'],fontsize=10)
plt.colorbar()
plt.xticks(range(len(df.columns)),df.columns,fontsize=10,rotation=90)
plt.tight_layout()
plt.show()


# In[827]:


PCA_vars = [0]*len(df_final.columns)

def ExtractColumn(lst,j): 
    return [item[j] for item in lst] 

for i, feature in zip(range(len(df.columns)),df.columns):
    x = ExtractColumn(pca.components_,i-1)
    if ((max(x) > 0.2) | (min(x) < -0.2)):
        if abs(max(x)) > abs(min(x)):
            PCA_vars[i] = max(x)
        else:
            PCA_vars[i] = min(x)                 
    else:
        PCA_vars[i] = 0

PCA_vars = pd.DataFrame(list(zip(df_final.columns,PCA_vars)),columns=('Name','Max absolute contribution'),index=range(1,41,1))      
PCA_vars = (PCA_vars[(PCA_vars['Max absolute contribution']!=0)]).sort_values(by='Max absolute contribution',ascending=False)
PCA_vars


# In[828]:


df_final.head()


# In[829]:


df.head()


# In[830]:


df_null = df[df.isnull().any(axis=1)]
Null_county = np.array(df_null.index.get_level_values('county'))


# In[831]:


df_estimation = df.drop(Null_county, level='county')

df_estimation.head()


# In[832]:


df_final_estimation = df_final.drop(Null_county, level='county')
df_final_estimation.head()


# In[833]:


Response_origin = pd.DataFrame(df_estimation['percentage20_Donald_Trump']) 

Response_origin.head()


# In[834]:


Response = pd.DataFrame(df_final_estimation['percentage20_Donald_Trump']) 
            # + df_final_estimation['percentage16_Donald_Trump']
             #, columns=["Response"])
        
Response = minmax_scaling(Response, columns=Response.columns)



# In[835]:


Response.head()


# In[836]:


votes = df_final.iloc[:,2:10].columns
votes


# In[837]:


df_estimation = df_estimation.drop(votes, axis=1)

df_estimation.head()


# In[838]:


df_final_estimation = df_final_estimation.drop(votes, axis=1)

df_final_estimation.head()


# In[839]:


x_train,x_test,y_train,y_test = train_test_split(df_final_estimation, Response,test_size=0.2,random_state=0)


# In[840]:


x_train_origin,x_test_origin,y_train_origin,y_test_origin = train_test_split(df_estimation, Response_origin,test_size=0.2,random_state=0)



# In[841]:


ModelAverage = y_train.mean()
print(str(round(ModelAverage,5)))


# In[842]:


ModelAverage_origin = y_train_origin.mean()
print(str(round(ModelAverage,5)))


# In[843]:


RMSE = y_test
RMSE.insert(1, "Model_Average_Trump", ModelAverage.values[0], True)
y_test=y_test.drop(['Model_Average_Trump'], axis=1)
RMSE.head(5)


# In[844]:


RMSE_origin = y_test_origin
RMSE_origin.insert(1, "Model_Average_Trump", ModelAverage_origin.values[0], True)
y_test_origin=y_test_origin.drop(['Model_Average_Trump'], axis=1)
RMSE_origin.head()


# In[845]:


y_train.head()


# In[846]:


x_train.head()


# In[847]:


Model_GLM = sm.GLM(y_train, x_train,family=sm.families.Gaussian())

Model_GLM_fit = Model_GLM.fit()


# In[848]:


print(Model_GLM_fit.summary())


# In[849]:


x_test.head()


# In[850]:


y_test.head()


# In[851]:


RMSE.insert(2, "Model_GLM_Trump", Model_GLM_fit.predict(x_test).values, True)


# In[852]:


RMSE.head()


# In[859]:


Model_RLM = sm.RLM(y_train, x_train)

Model_RLM_fit = Model_RLM.fit()



# In[860]:


print(Model_RLM_fit.summary())


# In[861]:


RMSE.insert(3, "Model_RLM_Trump", Model_RLM_fit.predict(x_test).values, True)


# In[862]:


RMSE.head()


# In[881]:



rmse1 = mean_squared_error(RMSE['Model_Average_Trump'], RMSE['percentage20_Donald_Trump'] ,squared=False)

print("Root mean square error for the average response is: ", rmse1)



# In[882]:



rmse2 = mean_squared_error(RMSE['Model_GLM_Trump'], RMSE['percentage20_Donald_Trump'] ,squared=False)


print("Root mean square error by using Generalized Linear Regression Model is: ", rmse2)



# In[899]:



rmse3 = mean_squared_error(RMSE['Model_RLM_Trump'], RMSE['percentage20_Donald_Trump'] ,squared=False)


print("Root mean square error by using Robust Linear Regression Model is: ", rmse3)


# ### Not Scaled Model below

# In[869]:


y_train_origin.head()


# In[870]:


x_train_origin.head()


# In[871]:


Model_GLM_origin = sm.GLM(y_train_origin, x_train_origin,family=sm.families.Gaussian())

Model_GLM_fit_origin = Model_GLM_origin.fit()


# In[872]:


print(Model_GLM_fit_origin.summary())


# In[873]:


x_test_origin.head()


# In[874]:


y_test_origin.head()


# In[875]:


RMSE_origin.insert(2, "Model_GLM_Trump", Model_GLM_fit_origin.predict(x_test_origin).values, True)


# In[876]:


RMSE_origin.head()


# In[877]:


Model_RLM_origin = sm.RLM(y_train_origin, x_train_origin)

Model_RLM_fit_origin = Model_RLM_origin.fit()


# In[878]:


print(Model_RLM_fit_origin.summary())


# In[879]:


RMSE_origin.insert(3, "Model_RLM_Trump", Model_RLM_fit_origin.predict(x_test_origin).values, True)


# In[884]:


RMSE_origin.head()


# In[891]:



rmse1_origin = mean_squared_error(RMSE_origin['Model_Average_Trump'], 
                                  RMSE_origin['percentage20_Donald_Trump'],squared=False)

print("Root mean square error for the average response is: ", rmse1_origin)


# In[893]:



rmse2_origin = mean_squared_error(RMSE_origin['Model_GLM_Trump'], 
                                  RMSE_origin['percentage20_Donald_Trump'],squared=False)


print("Root mean square error by using Generalized Linear Regression Model is: ", rmse2_origin)


# In[896]:



rmse3_origin = mean_squared_error(RMSE_origin['Model_RLM_Trump'], 
                                  RMSE_origin['percentage20_Donald_Trump'],squared=False)


print("Root mean square error by using Robust Linear Regression Model is: ", rmse3_origin)


# In[905]:


d_rmse = {'models': ['Average', 'GLM', 'RLM'],
          'not_scaled': [rmse1_origin, rmse2_origin, rmse3_origin],
          'scaled': [rmse1, rmse2, rmse3]}

df_rmse = pd.DataFrame(data = d_rmse,index=None)

print(df_rmse)


# In[909]:


Results = pd.DataFrame({'RMSE': [rmse1_origin,rmse2_origin,rmse3_origin],
                        'Name': ['Model_Average','Model_GLM','Model_RLM']})
Results = Results.set_index('Name')


plt.plot(Results)
plt.title("Root Mean Square Error of unscaled Models")
plt.ylabel('RMSE results')
plt.show()


# In[910]:


Results2 = pd.DataFrame({'RMSE': [rmse1,rmse2,rmse3],
                        'Name': ['Model_Average','Model_GLM','Model_RLM']})
Results2 = Results2.set_index('Name')

plt.plot(Results2)
plt.title("Root Mean Square Error of min max scaled Models")
plt.ylabel('RMSE results')
plt.show()


# In[ ]:





# In[ ]:




