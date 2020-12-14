#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np


# In[82]:


parse_dates = ['date']

covid_us_county = pd.read_csv("covid_us_county.csv", parse_dates=parse_dates, index_col=False)

covid_us_county = covid_us_county.drop('lat', 1)
covid_us_county = covid_us_county.drop('long', 1)

covid_us_county


# In[83]:


covid_us_states = covid_us_county.groupby(['state','state_code','date'], as_index=False).agg('sum').reset_index() 
covid_us_states = covid_us_states.drop('index', 1)
covid_us_states.to_csv("covid_us_states.csv", index=False)
covid_us_states


# In[ ]:





# In[227]:


parse_dates2 = ['date', 'lastUpdateEt', 'dateModified', 'checkTimeEt','dateChecked']

us_states_covid19_daily = pd.read_csv("us_states_covid19_daily.csv", parse_dates=parse_dates2, index_col=False)
us_states_covid19_daily.head()


# In[228]:


cols = ['date', 'state','positive','probableCases', 'negative',
        'totalTestResults','death','hospitalized', 'total']

us_states_covid19_daily_simple = us_states_covid19_daily[cols] #.fillna(0)
us_states_covid19_daily_simple


# In[229]:


covid_us_states


# In[261]:


covid_tigeryi = pd.merge(covid_us_states, us_states_covid19_daily_simple, how='inner', 
                      left_on=['state_code','date'], right_on = ['state','date'])


covid_tigeryi = covid_tigeryi.rename({'state_x': 'state'}, axis=1)
covid_tigeryi = covid_tigeryi.drop('state_y', 1)
covid_tigeryi = covid_tigeryi.drop('deaths', 1)
covid_tigeryi


# In[234]:


covid_tigeryi.loc[covid_tigeryi['state_code'] == 'NY']


# In[235]:


covid_tigeryi.to_csv("covid_tigeryi.csv", index=False)


# In[168]:


# dtypes = {'dem_2020': 'float', 'rep_2020': 'float', 'other_2020': 'float','Total 2016 Votes': 'float', 'Total 2020 Votes': 'float'}
popular_vote_by_states = pd.read_csv("popular_vote_by_states.csv") # , dtype=dtypes
popular_vote_by_states = popular_vote_by_states.drop('X', 1)
popular_vote_by_states = popular_vote_by_states.drop('Y', 1)
popular_vote_by_states = popular_vote_by_states.drop('State_num', 1)
popular_vote_by_states = popular_vote_by_states.drop('Center_X', 1)
popular_vote_by_states = popular_vote_by_states.drop('Center_Y', 1)
popular_vote_by_states.head()


# In[272]:


popular_vote_by_states["dem_percent"] = popular_vote_by_states["dem_2020"] / popular_vote_by_states["Total 2020 Votes"] * 100
popular_vote_by_states["rep_percent"] = popular_vote_by_states["rep_2020"] / popular_vote_by_states["Total 2020 Votes"] * 100
popular_vote_by_states["other_percent"] = popular_vote_by_states["other_2020"] / popular_vote_by_states["Total 2020 Votes"] * 100
popular_vote_by_states["dem_2020_margin"] = popular_vote_by_states["dem_percent"] - popular_vote_by_states["rep_percent"]
#popular_vote_by_states["vote_change"] = popular_vote_by_states["vote_change"] * 100
#popular_vote_by_states["2016 Margin"] = popular_vote_by_states["2016 Margin"] * 100
popular_vote_by_states["margin_shift"] = popular_vote_by_states["dem_2020_margin"] - popular_vote_by_states["2016 Margin"]
popular_vote_by_states["vote_change"] = (popular_vote_by_states["Total 2020 Votes"] - popular_vote_by_states["Total 2016 Votes"]) / popular_vote_by_states["Total 2016 Votes"] * 100  

popular_vote_by_states.head()


# In[273]:


popular_vote_by_states.to_csv("election_tigeryi.csv", index=False)


# In[253]:


parse_dates3 = ['modeldate']
presidential_poll_averages_2020 = pd.read_csv("presidential_poll_averages_2020.csv", parse_dates=parse_dates3)
presidential_poll_averages_2020 = presidential_poll_averages_2020.drop('cycle', 1)
presidential_poll_averages_2020 =  presidential_poll_averages_2020.drop('pct_estimate', 1)
presidential_poll_averages_2020


# In[254]:


presidential_poll_averages_2020 = presidential_poll_averages_2020.rename({'candidate_name': 'index'}, axis=1)
presidential_poll_pct_trend_adjusted = presidential_poll_averages_2020.pivot_table(index = ["state", "modeldate"],
                                           columns="index",
                                           values="pct_trend_adjusted").reset_index()
presidential_poll_pct_trend_adjusted = presidential_poll_pct_trend_adjusted.drop("Convention Bounce for Donald Trump", 1)
presidential_poll_pct_trend_adjusted = presidential_poll_pct_trend_adjusted.drop("Convention Bounce for Joseph R. Biden Jr.", 1)
presidential_poll_pct_trend_adjusted = presidential_poll_pct_trend_adjusted.rename({'modeldate': 'date'}, axis=1)
presidential_poll_pct_trend_adjusted = presidential_poll_pct_trend_adjusted.rename({'Donald Trump': 'rep_poll_2020'}, axis=1)
presidential_poll_pct_trend_adjusted = presidential_poll_pct_trend_adjusted.rename({'Joseph R. Biden Jr.': 'dem_poll_2020'}, axis=1)


# In[255]:


presidential_poll_pct_trend_adjusted["dem_lead"] = presidential_poll_pct_trend_adjusted["dem_poll_2020"] - presidential_poll_pct_trend_adjusted["rep_poll_2020"]
presidential_poll_pct_trend_adjusted


# In[258]:


presidential_poll_pct_trend_adjusted["dem_lead_rolling_7"] = presidential_poll_pct_trend_adjusted["dem_lead"].rolling(7, min_periods = 0).mean()

presidential_poll_pct_trend_adjusted


# In[260]:


presidential_poll_pct_trend_adjusted.to_csv("poll_tigeryi.csv", index=False)


# In[275]:


covid_tigeryi["positive_rate"] = covid_tigeryi["positive"] / covid_tigeryi["totalTestResults"] * 100
covid_tigeryi["positive_negative_ratio"] = covid_tigeryi["positive"] / covid_tigeryi["negative"] * 100
covid_tigeryi


# In[286]:


covid_tigeryi['positive_delta'] = covid_tigeryi['positive'] - covid_tigeryi['positive'].shift(1)
covid_tigeryi['negative_delta'] = covid_tigeryi['negative'] - covid_tigeryi['negative'].shift(1)
covid_tigeryi['totalTestResults_delta'] = covid_tigeryi['totalTestResults'] - covid_tigeryi['totalTestResults'].shift(1)
covid_tigeryi['death_delta'] = covid_tigeryi['death'] - covid_tigeryi['death'].shift(1)
covid_tigeryi["positive_rate_delta"] = covid_tigeryi["positive_delta"] / covid_tigeryi["totalTestResults_delta"] * 100
covid_tigeryi["positive_negative_ratio_delta"] = covid_tigeryi["positive_delta"] / covid_tigeryi["negative_delta"] * 100



covid_tigeryi.tail(10)


# In[284]:


covid_tigeryi.to_csv("covid_tigeryi.csv", index=False)


# In[241]:


covid_election_day_county = covid_us_county.loc[covid_us_county['date'] == '2020-11-03']
covid_election_day_county


# In[287]:



election_tigeryi = pd.read_csv("election_tigeryi.csv")
election_tigeryi.head()


# In[291]:


covid_election_day_county


# In[298]:


county_statistics = pd.read_csv("county_statistics.csv", index_col=None)



# In[299]:


county_statistics = county_statistics.drop('cases', 1)
county_statistics = county_statistics.drop('deaths', 1)


# In[306]:


county_statistics_merge = pd.merge(county_statistics, covid_election_day_county, how='left', 
                      left_on=['state','county'], right_on = ['state_code','county'])




# In[307]:


county_statistics_merge = county_statistics_merge.drop('state_code', 1)
county_statistics_merge = county_statistics_merge.rename({'state_x': 'state_code'}, axis=1)
county_statistics_merge = county_statistics_merge.rename({'state_y': 'state'}, axis=1)
county_statistics_merge = county_statistics_merge.drop('date', 1)



# In[313]:


county_statistics_merge = county_statistics_merge.dropna(subset=['percentage20_Donald_Trump','percentage20_Joe_Biden'], axis=0)
county_statistics_merge = county_statistics_merge.dropna(subset=['percentage16_Donald_Trump','percentage16_Hillary_Clinton'], axis=0)



# In[322]:


county_statistics_merge["percentage16_Donald_Trump"] = county_statistics_merge["votes16_Donald_Trump"] / county_statistics_merge["total_votes16"] * 100
county_statistics_merge["percentage16_Hillary_Clinton"] = county_statistics_merge["votes16_Hillary_Clinton"] / county_statistics_merge["total_votes16"] * 100
county_statistics_merge["percentage20_Donald_Trump"] = county_statistics_merge["votes20_Donald_Trump"] / county_statistics_merge["total_votes20"] * 100
county_statistics_merge["percentage20_Joe_Biden"] = county_statistics_merge["votes20_Joe_Biden"] / county_statistics_merge["total_votes20"] * 100




# In[328]:


county_statistics_merge["dem_16_margin"] = county_statistics_merge["percentage16_Hillary_Clinton"] - county_statistics_merge["percentage16_Donald_Trump"]
county_statistics_merge["dem_20_margin"] = county_statistics_merge["percentage20_Joe_Biden"] - county_statistics_merge["percentage20_Donald_Trump"]
county_statistics_merge["dem_margin_shift"] = county_statistics_merge["dem_20_margin"] - county_statistics_merge["dem_16_margin"]


# In[330]:


county_statistics_merge.to_csv("demographic_tigeryi.csv", index=False)


# In[329]:


county_statistics_merge


# In[335]:


usa_states_latitude_and_longitude = pd.read_csv("usa_states_latitude_and_longitude.csv")
us_lat_long = usa_states_latitude_and_longitude[['usa_state','usa_state_code', 'usa_state_latitude', 'usa_state_longitude']].dropna()


# In[339]:


election_tiger = pd.merge(election_tigeryi, us_lat_long, how='left', 
                      left_on=['state','stateid'], right_on = ['usa_state','usa_state_code'])




# In[341]:


election_tiger = election_tiger.rename({'stateid': 'state_code'}, axis=1)
election_tiger = election_tiger.drop('usa_state', 1)
election_tiger = election_tiger.drop('usa_state_code', 1)



# In[343]:


election_tiger.to_csv("election_tigeryi.csv", index=False)


# In[345]:


parse_dates = ['date']

poll_tigeryi = pd.read_csv("poll_tigeryi.csv", parse_dates=parse_dates)



# In[348]:


poll_tiger = pd.merge(poll_tigeryi, us_lat_long, how='left', 
                      left_on=['state'], right_on = ['usa_state'])



# In[351]:


poll_tiger = poll_tiger.drop('usa_state', 1)




# In[352]:


poll_tiger["dem_lead_rolling_30"] = poll_tiger["dem_lead"].rolling(30, min_periods = 0).mean()




# In[354]:


poll_tiger.to_csv("poll_tigeryi.csv", index=False)


# In[361]:


election_tiger2 = election_tiger[['state','called','dem_percent', 'rep_percent','dem_2020_margin']]

election_tiger2.head()


# In[359]:


poll_tiger.head()


# In[362]:


poll_tiger2 = pd.merge(poll_tiger, election_tiger2, how='left', 
                      left_on=['state'], right_on = ['state'])

poll_tiger2.head()


# In[366]:


poll_tiger2['dem_result_poll_diff'] = poll_tiger2['dem_percent'] - poll_tiger2['dem_poll_2020']
poll_tiger2['rep_result_poll_diff'] = poll_tiger2['rep_percent'] - poll_tiger2['rep_poll_2020']
poll_tiger2['dem_lead_result_poll_diff'] = poll_tiger2['dem_2020_margin'] - poll_tiger2['dem_lead']
poll_tiger2['dem_lead_rolling_7_diff'] = poll_tiger2['dem_2020_margin'] - poll_tiger2['dem_lead_rolling_7']
poll_tiger2['dem_lead_rolling_30_diff'] = poll_tiger2['dem_2020_margin'] - poll_tiger2['dem_lead_rolling_30']

poll_tiger2.head()


# In[369]:


poll_tiger2 = poll_tiger2.dropna(subset=['dem_percent','rep_percent'], axis=0)



# In[371]:


poll_tiger2.to_csv("poll_tigeryi.csv", index=False)


# In[372]:



county_statistics_merge = pd.read_csv("demographic_tigeryi.csv")

county_statistics_merge.head()


# In[381]:


county_statistics_merge['cases'] = county_statistics_merge['cases'].fillna(0)
county_statistics_merge['deaths'] = county_statistics_merge['deaths'].fillna(0)


# In[382]:


county_statistics_merge['cases_rate'] = county_statistics_merge['cases'] / county_statistics_merge['TotalPop'] * 100
county_statistics_merge['deaths_rate'] = county_statistics_merge['deaths'] / county_statistics_merge['TotalPop'] * 100
county_statistics_merge['men_percent'] = county_statistics_merge['Men'] / county_statistics_merge['TotalPop'] * 100
county_statistics_merge['women_percent'] = county_statistics_merge['Women'] / county_statistics_merge['TotalPop'] * 100


county_statistics_merge.head()


# In[383]:


county_statistics_merge.to_csv("demographic_tigeryi.csv", index=False)


# In[4]:


parse_dates = ['date']

covid_3 = pd.read_csv("covid_tigeryi.csv", parse_dates=parse_dates, index_col=False)


# In[5]:


covid_3.head(10)


# In[6]:


#pd.set_option('use_inf_as_na', True)

covid_3['positive_rate_delta'] = covid_3['positive_delta'] / covid_3['totalTestResults_delta'] * 100
covid_3['positive_negative_ratio_delta'] = covid_3['positive_delta'] / covid_3['negative_delta'] * 100

covid_3 = covid_3.replace(np.inf, np.nan)
#covid_3.replace(np.inf, np.nan)



# In[7]:


covid_3.head()


# In[8]:


covid_3.to_csv("covid_tigeryi.csv", index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




