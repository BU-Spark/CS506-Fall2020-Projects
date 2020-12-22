#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 22:22:43 2020

@author: stephanieforbes
"""

# data vis trial - wbur2018.csv  

import numpy as np 
import pandas as pd
from pandas import DataFrame
 

data = pd.read_csv("wbur2018.csv")
data_arr = data.to_numpy()

census_data = pd.read_csv("Revised Sub-Neighborhoods.csv")
areas = census_data.loc[:,'Neighborhood']

neighborhoods = [] # list of all neighborhoods according to census data 
"""can do this for sub-neighborhoods or whatever specificity is appropriate"""
for x in areas:
    if x == x: # removes nan values 
        if x not in neighborhoods:
            neighborhoods.append(x)
        
print(neighborhoods)
        
topics = pd.read_csv('topics.csv', header = None)
topics_arr = topics.to_numpy()


        

"""creating a way to count frequency for words mentioned""" 
# converts it to a list of strings
Words = []
for x in data_arr:
    Words.append(x[1])
        
table = [] #resulting table of each neighborhood with the number of times each topic appears
    
"""for neighborhood in neighborhoods:
    hood = [neighborhood]
    n = 0 #counter for each topic mention and neighborhood mention in same article 
    #for line in Words: # each article
     #   if line.count(neighborhood) > 0: #if neighborhood mentioned in article
    for topic in topics_arr: # for each topic 
        t = 0 #topic mention counter
        for x in topic: #for each word in each topic
            for line in Words:
                if line.count(neighborhood) > 0:
                    if line.count(x) > 0:
                        t += line.count(x)
                n += t
        hood.append(n)
    print("This is the length of hood: ", len(hood)) 
    print("This is the expected length of hood: ", len(topics)+1)              
    table.append(hood)
    """
    
for line in Words:
    for neighborhood in neighborhoods:
        if line.count(neighborhood) > 0:
            for topic in topics_arr:
                article_mention = [neighborhood]
                article_mention.append(topic[0])
                c = 0
                for x in topic[1:]:
                    c += line.count(x)
                    
                article_mention.append(c)
                table.append(article_mention)
print(table)
# find a way to prepend table with the name of each topic (value in position 0)

df = DataFrame(table, columns = ['Neighborhood','Topic', 'Frequency'])
df.to_csv('wbur2018_topic_frequency_3rd.csv')
                



