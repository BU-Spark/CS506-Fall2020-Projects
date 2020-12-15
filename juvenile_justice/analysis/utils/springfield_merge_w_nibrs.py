# Objective: merge the Springfield arrest logs with an FBI dataset called NIBRS,
# which contains information on the race and ethnicity of each person who is arrested
import numpy as np
import pandas as pd
import os

# Read in the datasets -- Springfield logs for 2017-2020, Massachusetts NIBRS data from 2017 and 2018
springfield_logs_path = os.path.join(os.path.dirname(os.path.abspath('')), 'datasets', 'springfield_arrest_logs.csv')
nibrs_2017_path = os.path.join(os.path.dirname(os.path.abspath('')), 'datasets', 'nibrs_2017.xlsx')
nibrs_2018_path = os.path.join(os.path.dirname(os.path.abspath('')), 'datasets', 'nibrs_2018.xlsx')

springfield_logs = pd.read_csv(springfield_logs_path)
nibrs_2017 = pd.read_excel(nibrs_2017_path)
nibrs_2018 = pd.read_excel(nibrs_2018_path)

# In the NIBRS data, keep only the columns which are shared by the 2017 and 2018 datasets, in order to merge them
# Want to keep Incident Date, County, Agency Name, Arrestee Seq, Arrest Date, Arrest Month, Arrestee Offense, Type of Arrest, 
# Arrestee Age, Arrestee Gender, Arrestee Race, Arrestee Ethnicity, and Disposition Under 18
nibrs_2017.drop(columns=['Substation'],inplace=True)
nibrs_2018.drop(columns=['ORI','Incident Number','BK_TIME','BRICArrestCode','BRIC Desc'],inplace=True)

# Merge the two NIBRS datasets to create a combined 2017-2018 file
nibrs_all = pd.concat([nibrs_2017, nibrs_2018])
# Drop all towns other than Springfield
nibrs_all = nibrs_all[nibrs_all['Agency Name']=='Springfield']
# Set up a fresh numerical index
nibrs_all.set_index(np.array(range(len(nibrs_all))),inplace=True)
# Make all of the NIBRS dates into a uniform format
nibrs_all['Arrest Date'] = nibrs_all['Arrest Date'].apply(lambda x: pd.to_datetime(x).date())
# Do the same date-cleaning procedure for Springfield
springfield_logs['Arrest Date'] = springfield_logs['Arrest Date/Time'].apply(lambda x: pd.to_datetime(x).date())
springfield_logs.rename(columns={'Suspect Age on Date of Arrest':'Arrestee Age'},inplace=True)

# Drop Springfield logs data which did not come from 2017 or 2018
springfield_logs = springfield_logs[springfield_logs['Arrest Date']<pd.to_datetime('2019-01-01')]

# Sort the NIBRS dataset, as well as the Springfield dataset, by date and arrestee age to prepare for merging
nibrs_all.sort_values(by=['Arrest Date','Arrestee Age'],inplace=True)
springfield_logs.sort_values(by=['Arrest Date','Arrestee Age'],inplace=True)

# Set up an 'IDENTIFIER' column in each dataset to hold both date and age,
# to help me find extraneous records from either dataset
nibrs_all['IDENTIFIER'] = nibrs_all.apply(lambda x: str(x['Arrest Date']) + ' ' + str(x['Arrestee Age']) ,axis=1)
springfield_logs['IDENTIFIER'] = springfield_logs.apply(lambda x: str(x['Arrest Date']) + ' ' + str(x['Arrestee Age']) ,axis=1)

# We're only going to merge the records in the Springfield dataset which can be
# perfectly matched to a record in NIBR

# Figure out which date-age combos are duplicated in each dataset
springfield_duplicates = springfield_logs[springfield_logs.duplicated(subset=['IDENTIFIER'], keep=False)]
nibrs_duplicates = nibrs_all[nibrs_all.duplicated(subset=['IDENTIFIER'], keep=False)]
# Grab only the records which are unique within their respective datasets
springfield_unique = springfield_logs[~springfield_logs['IDENTIFIER'].isin(springfield_duplicates['IDENTIFIER'])]
nibrs_unique = nibrs_all[~nibrs_all['IDENTIFIER'].isin(nibrs_duplicates['IDENTIFIER'])]

# Keep only the NIBRS records which have at least one date-age match in the Springfield logs
nibrs_overlap_only = nibrs_unique[nibrs_unique['IDENTIFIER'].isin(springfield_unique['IDENTIFIER'])]
# Keep only the Springfield records which have at least one date-age match in the NIBRS files
springfield_overlap_only = springfield_unique[springfield_unique['IDENTIFIER'].isin(nibrs_unique['IDENTIFIER'])]

# DESCRIPTION OF THE MERGING PROCESS
# To end up in the merge_output dataframe, an arrest from the Springfield dataset has to meet two criteria:
# 1) its date-age combo is unique in the Springfield dataset
# 2) its date-age combo has exactly one match in the NIBRS dataset

# Merge the two datasets, using only those Springfield 
merge_output = springfield_unique.merge(nibrs_unique,how='inner',on='IDENTIFIER')

# Save the output from the merging process for a race/ethnicity equity analysis to be done in another file
merge_output.to_csv('springfield_nibrs_merged.csv')
