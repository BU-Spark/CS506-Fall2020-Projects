#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 14:07:21 2020

@author: raphaelbruni
"""

# Author: Raphael Bruni
# Course: CAS CS 506 A1
# File Name: Code for CfJJ Project
# File Description: Code that has allowed for an analysis to be conducted
# on New Bedford police data. Most of the functions produce lists or statistics
# that allowed for an analysis to be conducted. Code written in R, which is
# included in this file, produced some plots.

# read_listings: takes in the New Bedford dataset (filename) and creates a 
# list of lists storing the features of the dataset.
def read_listings(filename):
    
    # Create an empty list to store the data.
    data = []
    
    # Open the file.
    with open(filename, 'r') as f:
        # Skip the first line of the file.
        next(f)
        start = 0
        # Read the lines in the file.
        lines = f.readlines()
        start = 1
        # Iterate over each line in the file.
        for line in lines:
            # Create an empty list to store the data of every row.
            empty = []
            # Split each line by commas.
            temp = line.split(',')
            count = 0
            # Replace the '\n' at the end of each line with a blank space. 
            data.append(str(temp[-1].replace('\n','')))
            # Iterate over each entry in the line.
            for ind, entry in enumerate(temp):
                # Append every value of each feature to the list.    
                if count == 0:
                    if entry != '':
                        num = int(entry)
                        empty.append(num)
                        count += 1
                    else:
                        empty.append("NaN")
                        count += 1
                elif count == 1:
                    if entry != '':
                        num = int(entry)
                        empty.append(num)
                        count += 1
                    else:
                        empty.append("NaN")
                        count += 1
                elif count == 2:
                    if entry != '':
                        num = str(entry)
                        empty.append(num)
                        count += 1
                    else: 
                        empty.append("NaN")
                        count += 1
                elif count == 3:
                    if entry != '':
                        num = str(entry)
                        empty.append(num)
                        count += 1
                    else:
                        empty.append("NaN")
                        count += 1
                elif count == 4:
                    if entry != '':
                        num = str(entry)
                        empty.append(num)
                        count += 1
                    else:
                        empty.append("NaN")
                        count += 1
                elif count == 5:
                    if entry != '':
                        num = str(entry)
                        empty.append(num)
                        count += 1
                    else:
                        empty.append("NaN")
                        count += 1
                elif count == 6:
                    if entry != '':
                        num = str(entry)
                        empty.append(num)
                        count += 1
                    else:
                        empty.append("NaN")
                        count += 1
                elif count == 7:
                    if entry != '':
                        num = str(entry)
                        empty.append(num)
                        count += 1
                    else:
                        empty.append("NaN")
                        count += 1
                elif count == 8:  
                    if entry != '':
                        num = str(entry)
                        empty.append(num)
                        count += 1
                    else:
                        empty.append("NaN")
                        count += 1
                elif count == 9:
                    if entry != '':
                        num = int(entry)
                        empty.append(num)
                        count += 1
                    else:
                        empty.append("NaN")
                        count += 1
                elif count == 10:
                    if entry != '':
                        num = int(entry)
                        empty.append(num)
                        count += 1
                    else:
                        empty.append("NaN")
                        count += 1
                        
                elif count == 11:
                    if entry != '':
                        num = str(entry)
                        empty.append(num)
                        count += 1
                    else: 
                        empty.append("NaN")
                        count += 1
                elif count == 12:
                    if entry != '':
                        num = str(entry)
                        empty.append(num)
                        count += 1
                    else: 
                        empty.append("NaN")
                        count += 1
             
            # Append the row of data to the complete list.   
            data.append(empty)
            
            start += 1        
    
    
    # Create a list called samples.
    samples = []
    # Iterate over each row in the dataset, and append every other row of 
    # data from the dataset to samples.
    for entry in range(len(data)):
        if entry % 2 != 0:
            samples.append(data[entry])
    # Return the refined dataset.
    return samples


# get_names: takes in no inputs, and return two lists, one storing the 
# first names of the police officers in the New Bedford dataset, and the 
# other storing the last names of the police officers in the New 
# Bedford dataset
def get_names():
    # Store the data in a list of lists.
    data = read_listings("New Bedford Officer Names.csv")
    # Create two lists to store the first abd last names of the police 
    # officers.
    last_names = []
    first_names = []
    
    # Iterate over each row in the dataset, and append each unique first name
    # and last name to their respective lists.
    for x in range(len(data)):
        if data[x][-1] not in last_names:
            last_names.append(data[x][-1])
            first_names.append(data[x][-2])
           
    
    # Iterate over each entry in last_names, and remove any entries that
    # should not belong in the lists storing the names.
    for entry in range(len(last_names) - 2):
        
        if last_names[entry] == ')' or last_names[entry] == '9':
            last_names.remove(last_names[entry])
            first_names.remove(first_names[entry])
       
    # Return the lists storing the names.
    return first_names, last_names
    

# races: takes in no inputs and returns two lists, one storing the unique
# races of the civilians in the New Bedford dataset, and the other storing
# the unique ethnicities of the civilians in the New Bedford dataset.
def races():
    # Store the data in a list of lists.
    data = read_listings("New Bedford Officer Names.csv")
    # Create two lists, one that will store the races of the civilians in
    # the New Bedford dataset, and the other that will store the ethnicities of
    # the civilians in the New Bedford dataset
    races = []
    ethnicities = []
    # Iterate over each observation in the dataset.
    for x in range(len(data)):
        # Append each of the unique races to the races list.
        if data[x][7] not in races:
            races.append(data[x][7])
    # Iterate over each observation in the dataset.
    for x in range(len(data)):
        # Append each of the unique ethnicities to the ethnicities list.
        if data[x][8] not in ethnicities:
            ethnicities.append(data[x][8])
    # Return the lists storing the races and ethnicities.
    return races, ethnicities
    

   
# count_races: takes in no inputs, and prints statistics describing the 
# percentage of incidents in the New Bedford dataset involving people of
# specific races.    
def count_races():
    # Store the data in a list of lists.
    data = read_listings("New Bedford Officer Names.csv")
    # Create a list of counts that stores the number of counts of each of
    # the unique races in the New Bedford dataset.
    counts = [0,0,0,0,0,0]
    # Iterate over each observation in the dataset, and count the number
    # of each race in the dataset. Note that the race of white Hispanics 
    # is considered to be "Hispanic", while the race of black Hispanics is
    # considered to be "black".
    for x in range(len(data)):
        if data[x][7] == 'W' and data[x][8] == 'H':
            counts[5] += 1
        elif data[x][7] == 'W' and data[x][8] != 'H':
            counts[0] += 1
        elif data[x][7] == 'B':
            counts[1] += 1
        elif data[x][7] == 'U':
            counts[2] += 1
        elif data[x][7] == 'P':
            counts[3] += 1
        elif data[x][7] == 'A':
            counts[4] += 1
        elif data[x][8] == 'H' and data[x][7] != 'B':
            counts[5] += 1
    # Count the number of unique civilians in the dataset.
    total = 0
    for x in range(len(counts)):
        total += counts[x]
    
    # Print the number of unique incidents in the New Bedford dataset.
    print('There were ' + str(total) + ' incidents in New Bedford.\n')
    # Calculate proportions of incidents involving blacks, whites, Asians,
    # and Hispanics.
  
    black_prop = (counts[1]/total) * 100
    white_prop = (counts[0]/total) * 100
    asian_prop = (counts[4]/total) * 100
    hisp_prop = (counts[5]/total) * 100
    # Print the proportion of incidents involving people who are black,
    # white, Asian, and Hispanic.
    print(str(round(black_prop, 2)) + ' % of the incidents involved black civilians.\n')
    print(str(round(white_prop, 2)) + ' % of the incidents involved non-Hispanic white civilians.\n')
    print(str(round(asian_prop, 2)) + ' % of the incidents involved Asian civilians.\n')
    print(str(round(hisp_prop, 2)) + ' % of the incidents involved Hispanic civilians.\n')
  
        
# officers: takes in no inputs, and return two lists, one storing the last
# names of police officers involved with at least 95 unique civilians in the
# New Bedford dataset, and another storing their first names.
def officers():
    # Store the data in a list of lists.
    data = read_listings("New Bedford Officer Names.csv")
    # Create empty lists to store the number of incidents each police officer
    # in the dataset is involved in, as well as their first and last names.
    officers = []
    first_names = []
    last_names = []
    # Iterate over each observation in the dataset.
    for x in range(len(data)):
        # Append the unique names of the officers to their respective lists,
        # as well as number slots for the number of incidents they're involved
        # in.
        if data[x][12] not in last_names:
            last_names.append(data[x][12])
            first_names.append(data[x][11])
            officers.append(0)

    # Iterate over each observation in the data, and, using the index of the
    # list storing the officers' last names, increment the number of incidents
    # each officer is involved in.
    for y in range(len(data)):
        i = last_names.index(data[y][12])
        officers[i] += 1
    # Create lists to store the first and last names of officers who are 
    # involved in a high number of incidents.
    common_officers_last = []
    common_officers_first = []
    # Iterate over each observation in the dataset, and account for each 
    # officer whose name occurs at least 95 times in the dataset
    for x in range(len(officers)):
        if officers[x] >= 95:
            common_officers_last.append(last_names[x])
            common_officers_last.append(officers[x])
            common_officers_first.append(first_names[x])
    
    # Return the last names of officers involved with many civilains (and
    # the number of incidents they're involved in), as well as their first names.
    return common_officers_last, common_officers_first
    
    
# officers_blacks: takes in no inputs and return two lists, one storing the last
# names of police officers involved with at least 47 unique black civilians in the
# New Bedford dataset, and another storing their first names.       
def officers_blacks():
    # Store the data in a list of lists.
    data = read_listings("New Bedford Officer Names.csv")
    # Create empty lists to store the number of incidents each police officer
    # in the dataset is involved in, as well as their first and last names.
    officers = []
    first_names = []
    last_names = []
    # Iterate over each observation in the dataset.
    for x in range(len(data)):
        # Append the unique names of the officers to their respective lists,
        # as well as number slots for the number of incidents they're involved
        # in.
        if data[x][12] not in last_names:
            last_names.append(data[x][12])
            first_names.append(data[x][11])
            officers.append(0)

    # Iterate over each observation in the dataset.
    for y in range(len(data)):
        # Keep track of the names all of the police officers involved in 
        # incidents' involving black individuals.
        if data[y][7] == 'B':
            i = last_names.index(data[y][12])
            officers[i] += 1
    # Create empty lists that can store the first and last names of police
    # officers involved in a high number of incidents' involving black
    # civilians.
    common_officers_last = []
    common_officers_first = []
    # Keep track of the names of officer involved with at least 47
    # unique black civilians. 
    for x in range(len(officers)):
        if officers[x] >= 47:
            common_officers_last.append(last_names[x])
            common_officers_last.append(officers[x])
            common_officers_first.append(first_names[x])
    # Return the last names of officers involved with many black civilains (and
    # the number of such incidents they're involved in), as well as their 
    # first names.
    return common_officers_last, common_officers_first
   
# officers_blacks: takes in no inputs and return two lists, one storing the last
# names of police officers involved with at least 23 unique Hispanic civilians in the
# New Bedford dataset, and another storing their first names. 
def officers_hispanics():
    # Store the data in a list of lists.
    data = read_listings("New Bedford Officer Names.csv")
    # Create empty lists to store the number of incidents each police officer
    # in the dataset is involved in, as well as their first and last names.
    officers = []
    first_names = []
    last_names = []
    # Iterate over each observation in the dataset.
    for x in range(len(data)):
        # Append the unique names of the officers to their respective lists,
        # as well as number slots for the number of incidents they're involved
        # in.
        if data[x][12] not in last_names:
            
            last_names.append(data[x][12])
            first_names.append(data[x][11])
            officers.append(0)
    # Iterate over each observation in the dataset.
    for y in range(len(data)):
        # Keep track of the names all of the police officers involved in 
        # incidents' involving black individuals.
        if data[y][8] == 'H' and data[y][7] == 'W':
            i = last_names.index(data[y][12])
            officers[i] += 1
        elif data[y][8] == 'H' and data[y][7] != 'B':
            i = last_names.index(data[y][12])
            officers[i] += 1
    
    # Create empty lists that can store the first and last names of police
    # officers involved in a high number of incidents' involving Hispanic
    # civilians.
    common_officers_last = []
    common_officers_first = []
    # Keep track of the names of officer involved with at least 23
    # unique Hispanic civilians. 
    for x in range(len(officers)):
        if officers[x] >= 23:
            common_officers_last.append(last_names[x])
            common_officers_last.append(officers[x])
            common_officers_first.append(first_names[x])
   
    # Return the last names of officers involved with many Hispanic civilains (and
    # the number of such incidents they're involved in), as well as their 
    # first names.
    return common_officers_last, common_officers_first
   
 
# sex(): takes in no inputs and prints statements describing the fraction
# of incidents in the New Beford dataset that involve each of the sexes
# (female, male, unkown/other).
def sex(): 
    # Store the data in a list of lists.
    data = read_listings("New Bedford Officer Names.csv")
    # Create an empty list to store the sexes of the individuals in the 
    # New Bedford dataset.
    sex = []
    # Iterate over each observations in the dataset.
    for x in range(len(data)):
        # If a sex is not in the sex list, append it to that list..
        if data[x][6] not in sex:
            sex.append(data[x][6])
  
    
    total = 0
    # Create a list called genders which accounts for the total number of
    # incidents involving each of the sexes in the dataset (female, male, and
    # unknown/other).
    genders = [0,0,0]
    # Increment each index in the genders list based on the sex of the
    # individual.
    for x in range(len(data)):
        if data[x][6] == 'M':
            genders[0] += 1
        elif data[x][6] == 'F':
            genders[1] += 1
        else:
            genders[2] += 1
    # Compute the total number of unique civilians in the dataset.
    for x in range(len(genders)):
        total += genders[x]
    # Compute proportions of the representation of the sexes in the dataset.
    male_prop = (genders[0]/total) * 100
    female_prop = (genders[1]/total) * 100
    other_prop = (genders[2]/total) * 100
    # Print statements describing the percentage of incidents involivng each
    # of the sexes.
    print(str(round(male_prop,2)) + '% of the incidents involved male civilians.\n')
    print(str(round(female_prop,2)) + '% of the incidents involved female civilians.\n')      
    print(str(round(other_prop,2)) + '% of the incidents involved neither male nor female civilians.\n')   


# age: takes in no inputs and calculates the representation of the New Bedford
# dataset of people in three specific age groups: 10-year-olds through 
# 17-year-olds, 18-year-olds through 20-year-olds, and 21-year-olds through 
# 25-year-olds
def age():
    # Store the data in a list of lists.
    data = read_listings("New Bedford Officer Names.csv")
    
    black_count = 0
    # Count the number of incidents in the dataset that involve black civilians.
    for entry in range(len(data)):
        if data[entry][7] == 'B':
            black_count += 1
    ten_18 = 0
    eighteen_20 = 0
    twenty_25 = 0
    # Kepp track of the number of incidents in the dataset that involve 
    # people in three specific age groups: 10-year-olds through 17-year-olds,
    # 18-year-olds through 20-year-olds, and 21-year-olds through 25-year-olds
    for entry in range(len(data)):
        if data[entry][9] == 'NaN':
            continue
        
        if data[entry][9] < 18 and data[entry][9] >= 10:
            ten_18 += 1
        elif data[entry][9] <= 20:
            eighteen_20  += 1
        elif data[entry][9] <= 25:
            twenty_25 += 1
    # Return the counts of the representaton of the three age groups.
    return ten_18, eighteen_20, twenty_25


# age_groups_1: takes in no inputs and returns a list of police officers in
# the New Bedford dataset who were involved in at least 47 incidents involving
# people aged between 10-year-olds and 17-year-olds, as well as a count of
# the number of incidents these officers were involved in with these individuals.
def age_groups_1():
    # Store the data in a list of lists.
    data = read_listings("New Bedford Officer Names.csv")
    # Create a list that will store the name of police officers who are
    # commonly involved in incidents involving civilains who are between
    # 10 years old and 17 years old.
    common_officers = []
    last_names = []
    officers = []
    # Iterate over each observation in the datset and account for each unique
    # police officer in the datset.
    for x in range(len(data)):
        if data[x][12] not in last_names:
            last_names.append(data[x][12])
            officers.append(0)
    count = 0
    # Iterate over each observation in the datset, and for each civilian
    # in the age group of interest, increment the count for officer involved
    # in the incident.
    for x in range(len(data)):
        if data[x][9] != "NaN":
            if data[x][9] >= 10 and data[x][9] <= 17:
                count += 1
                
                i = last_names.index(data[x][12])
                officers[i] += 1
    # Create a list of common officers involved with the age group.
    common_officers = []
    # For each officer involved in at least 47 incidents involing people in the
    # age group, appen their name to the list.
    for x in range(len(officers)):
        if officers[x] >= 47:
            
            common_officers.append(last_names[x])
    # Return the list of common officers and the total count of incidents
    # the officers in the list were involved in with people in the age group.
    return common_officers, count
        

# age_groups_2: takes in no inputs and returns a list of police officers in
# the New Bedford dataset who were involved in at least 47 incidents involving
# people aged between 18-year-olds and 20-year-olds, as well as a count of
# the number of incidents these officers were involved in with these individuals.
def age_groups_2():
     # Store the data in a list of lists.
    data = read_listings("New Bedford Officer Names.csv")
    # Create a list that will store the name of police officers who are
    # commonly involved in incidents involving civilains who are between
    # 18 years old and 20 years old.
    common_officers = []
    last_names = []
    officers = []
    # Iterate over each observation in the datset and account for each unique
    # police officer in the datset.
    for x in range(len(data)):
        if data[x][12] not in last_names:
            last_names.append(data[x][12])
            officers.append(0)
    count = 0
    # Iterate over each observation in the datset, and for each civilian
    # in the age group of interest, increment the count for officer involved
    # in the incident.
    for x in range(len(data)):
        
        if data[x][9] != "NaN":
            if data[x][9] >= 18 and data[x][9] <= 20:
               
                count += 1
                i = last_names.index(data[x][12])
                officers[i] += 1
    # Create a list of common officers involved with the age group.
    common_officers = []
    # For each officer involved in at least 41 incidents involing people in the
    # age group, appen their name to the list.
    for x in range(len(officers)):
        if officers[x] >= 41:
            
            common_officers.append(last_names[x])
    # Return the list of common officers and the total count of incidents
    # the officers in the list were involved in with people in the age group.
    return common_officers, count
           
            
def age_groups_3():
    data = read_listings("New Bedford Officer Names.csv")
    common_officers = []
    last_names = []
    officers = []
    for x in range(len(data)):
        if data[x][12] not in last_names:
            last_names.append(data[x][12])
            officers.append(0)
    count = 0
    for x in range(len(data)):
       
        if data[x][9] != "NaN":
            if data[x][9] >= 21 and data[x][9] <= 25:
                
                count += 1
                i = last_names.index(data[x][12])
                officers[i] += 1
    common_officers = []
    for x in range(len(officers)):
        if officers[x] >= 43:
            print(last_names[x])
            print(officers[x])
            common_officers.append(last_names[x])
 
    return common_officers, count  

# Code done in R:

#library(tidyverse)
#setwd("~/Desktop")
#New_Bedford <- read_csv("field_incident_reports.csv")
#true_race <- function(x,y) {
  #if (x == "W" & y == "H") {
  #  "H"
 # } else if (x == "B") {
 #   "B"
 # } else if (x == "W" & y != "H") {
 #   "W"
 # } else if (x == "U") {
 #   "U"
 # } else if (x == "P") {
 #   "P"
 # } else if (x == "A") {
 #   "A"
 # } else if (x != "B" & y == "H") {
  #  "H"
 # }
  
#}
#New_Bedford <- New_Bedford %>% group_by(RACE,Ethnicity) %>% mutate(real_race = true_race(RACE, Ethnicity))
#ggplot(data = New_Bedford) + geom_bar(mapping = aes(x = real_race, fill = SEX)) + xlab("Race") + scale_x_discrete("Race", labels = c("A" = "Asian", "B" = "Black", "H" = "Hispanic", "P" = "Pac Isl", "U" = "Unknown", "W" = "White"))  + ylab("Number of Individuals") + ggtitle("New Bedford Incidents by Race")

#revise <- New_Bedford %>% group_by(X1) %>% mutate(demographic = X1)
#revise$demographic <- 1:nrow(revise)

#dem_rep <- function(x) {
#  if (x <= 3265) {
 #   "W" 
 # } else if (x <= 3594) {
  #  "B"
  #} else if (x <= 3668) {
  #  "A"
  #} else if (x <= 3669) {
  #  "P"
  #} else if (x <= 4408) {
  #  "H"
 # } else {
  #  "U"
 # }
#}

#revise <- revise %>% group_by(demographic) %>% mutate(dem_race = dem_rep(demographic))

#ggplot(data = revise) + geom_bar(mapping = aes(x = dem_race, fill = SEX)) + xlab("Race") + scale_x_discrete("Race", labels = c("A" = "Asian", "B" = "Black", "H" = "Hispanic", "P" = "Pac Isl", "U" = "Unknown", "W" = "White"))  + ylab("Number of Individuals (Adjusted for Population Sizes)") + ggtitle("New Bedford Racial Demographics")
    
    