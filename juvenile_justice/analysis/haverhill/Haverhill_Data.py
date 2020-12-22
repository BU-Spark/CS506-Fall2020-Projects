#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:39:59 2020

@author: raphaelbruni
"""
# Author: Raphael Bruni
# Course: CAS CS 506 A1
# File Name: Code for Haverhill Component of CfJJ Project
# File Description: Code that has allowed for an analysis to be conducted
# on Haverhill school data. Most of the functions produce lists or statistics
# that allowed for an analysis to be conducted. 

# import csv to read a csv file.
import csv


# read_listings: takes in no inputs and returns a list of lists containing the
# Haverhill data.
def read_listings():
    # Create a list to store the data.
    data = []
    # Open the Haverhill CSV file.
    with open('Clean_Haverhill.csv', 'r') as file:
        # Read the file.
        reader = csv.reader(file)
        count = 0
        # Iterate over each row in the file, making sure to append the first
        # 249 rows (the rows that contain the data.)
        for row in reader:
            if count <= 249:
                data.append(row)
                count += 1
    # Return the data.
    return data


            
# off_race: takes in the Haverhill data, data, and returns the unique
# values for the races and sexes of the offenders in the dataset.
def off_race(data):
    # Create lists to store the values.
    race = []
    sex = []
    # Get all of the data except the first row (the column titles).
    data = data[1::]
    # Iterate over each row in the dataset.
    for row in range(len(data)):
        
        count = 0
        # Iterate over each entry in each row.
        for entry in range(len(data[0])):
            # If the value in the offender race column is not in the race list,
            # append it to the list.
            if count == 7 and data[row][entry] not in race:
                race.append(data[row][entry])
            # If the value in the offender sex column is not in the sex list,
            # append it to the list.
            if count == 8 and data[row][entry] not in sex:
                sex.append(data[row][entry])
            count += 1
                
    # Return the two lists.
    return race, sex

# race: takes in the Haverhill data, data, and returns counts of each of the
# unique entries in the offender race column.
def race(data):
    # Create a list to store the different entries in the offender race column.
    race = []
    # Get all of the data except the first row (the column titles).
    data = data[1::]
    # Iterate over each row in the dataset.
    for row in range(len(data)):
        count = 0
        # Iterate over each entry in each row.
        for entry in range(len(data[0])):
            # Append the value in the offender race column to the race list.
            if count == 7:
                race.append(data[row][entry])
            count += 1
    # Initialize values for the three unique values in the offender race list
    # (question marks, Blacks, and whites).
    question_count = 0
    black_count = 0
    white_count = 0
    
    # Iterate over each entry in the race list, and increment each count 
    # variable by one every time the iteration comes across the corresponding
    # entry.
    for entry in range(len(race)):
        if race[entry] == "WHITE":
            white_count += 1
        elif race[entry] == "BLACK":
            black_count += 1
        elif race[entry] == "?":
            question_count += 1
    # Return the counts.
    return question_count, black_count, white_count
    
# officers: takes in the Haverhill data, data, and returns lists of the unique
# police officers in the dataset and their representation in the data, as well
# as a number of the different officers in the dataset.
def officers(data):
    # Create a list to store the unique names of the police officers.
    officers = []
    # Create a list to store the counts of the police officers.
    officers_counts = []
    # Get all of the data except the first row (the column titles).
    data = data[1::]
    # Iterate over each row in the dataset.
    for row in range(len(data)):
        count = 0
        # Iterate over each entry in each row.
        for entry in range(len(data[0])):
            # If the officer's name is not in the officers list, append it
            # to the list, and append a value of 0 to the officers_counts list.
            if count == 9 and data[row][entry] not in officers:
                officers.append(data[row][entry])
                officers_counts.append(0)
            count += 1  
    # Iterate over each row in the dataset.
    for row in range(len(data)):
        # Get the index of each officer from the officers list, and increment
        # the corresponding value in officers_counts by one.
        i = officers.index(data[row][9])
        officers_counts[i] += 1
    # Return the two lists as well as the number of different officers 
    # (len(officers)).
    return officers_counts, officers, len(officers)

# offender_sex_count: takes in the Haverhill data, data, and returns a list of
# the representation of the sexes of the offenders in the dataset.
def offender_sex_count(data):
    # Create a list to store the unique sexes.
    sexes = []
    # Create a list to store counts of the sexes.
    sexes_counts = []
    # Get all of the data except the first row (the column titles).
    data = data[1::]
    # Iterate over each row in the dataset.
    for row in range(len(data)):
        count = 0
        # Iterate over each entry in each row.
        for entry in range(len(data[0])):
            # If the entry for the offender sex is not in the sexes list, 
            # append it to the list, and append a value of zero the sexes_counts
            # list.
            if count == 8 and data[row][entry] not in sexes:
                sexes.append(data[row][entry])
                sexes_counts.append(0)
            count += 1
    # Iterate over each row in the dataset.
    for row in range(len(data)):
        # Get the index of each offender sex from the offender sex list,
        # and increment the corresponding value in sexes_counts by one.
        i = sexes.index(data[row][8])
        sexes_counts[i] += 1
    # Return the sexes_counts list.
    return sexes_counts
    
# offender_race_count: takes in the Haverhill data, data, and returns a list of
# the representation of the races of the offenders in the dataset.
def offender_race_count(data):
    # Create a list to store the unique races.
    races = []
    # Create a list to store counts of the races.
    races_counts = []
    # Get all of the data except the first row (the column titles).
    data = data[1::]
    # Iterate over each row in the dataset.
    for row in range(len(data)):
        count = 0
        # Iterate over each entry in each row.
        for entry in range(len(data[0])):
            # If the entry for the offender race is not in the races list, 
            # append it to the list, and append a value of zero the races_counts
            # list.
            if count == 7 and data[row][entry] not in races:
                races.append(data[row][entry])
                races_counts.append(0)
            count += 1
    # Iterate over each row in the dataset.
    for row in range(len(data)):
        # Get the index of each offender race from the offender race list,
        # and increment the corresponding value in races_counts by one.
        i = races.index(data[row][7])
        races_counts[i] += 1
    # Return the races_counts list.
    return races_counts
    