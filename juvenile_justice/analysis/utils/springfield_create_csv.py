import numpy as np
import pandas as pd
import tika
from tika import parser
import os
import requests

# Out of all the PDF-text-parsing libraries I've tried, this one reads this particular
# set of PDFs into a format that is most useful to me
tika.initVM()

# PART 1: SET UP ALL FUNCTIONS THAT ARE NEEDED TO EXTRACT INFO FROM THE REPORTS IN PDF FORM

# Extract the text in the file and begin by removing excess whitespace
def get_text_from_tika(tika_output):
    split_data = tika_output['content'].split('\n')
    new_string = ''
    for i in range(len(split_data)):
        if split_data[i] == '' or split_data[i] == ' ':
            continue
        else:
            new_string += split_data[i].strip() + '\n'
    return new_string.split('\n')

# Build a new list that contains only the actual report information
def clean_top_bottom(lines):
    trim_top_bottom = []
    # Figure out where the background info at the very beginning of the document ends
    for i in range(len(lines)):
        if "Det.  ID" in lines[i] or "Det. ID" in lines[i] or "Det.   ID" in lines[i]:
            records_start_index = i
            break
    # Figure out where the totals info at the end starts
    for i in range(len(lines)):
        if "Totals" in lines[i] and '--------' in "".join([lines[i] for i in range(i,len(lines))]):
            totals_info_index = i
            break
    # Drop the "filler" info at the top and bottom of the document
    for i in range(len(lines)):
        if i in range(records_start_index,totals_info_index):
            trim_top_bottom.append(lines[i])
    no_headers = []
    # Drop extra lines in the remaining text which are unrelated to any specific arrest report
    for j in range(len(trim_top_bottom)):
        if 'Page:' in trim_top_bottom[j] or 'Thru:' in trim_top_bottom[j]:
            continue
        elif 'A ->' in trim_top_bottom[j] or 'J ->' in trim_top_bottom[j] or 'R ->' in trim_top_bottom[j]:
            continue
        elif j != 0 and ('A ->' in trim_top_bottom[j-1] and 'Approved' in trim_top_bottom[j]):
            continue
        elif j != 0 and ('J ->' in trim_top_bottom[j-1] and 'Juvenile' in trim_top_bottom[j]):
            continue
        elif j != 0 and ('R ->' in trim_top_bottom[j-1] and 'Released' in trim_top_bottom[j]):
            continue
        else:
            no_headers.append(trim_top_bottom[j])
    return no_headers

# Figure out which indices correspond to the starts of records
def get_record_and_offenses_indices(no_headers):
    record_start_indices = []
    offenses_start_indices = []
    for i in range(len(no_headers)):
        # Find the indices in no_headers which correspond to the first line of an arrest report
        if "Det.  ID" in no_headers[i] or "Det. ID" in no_headers[i] or "Det.   ID" in no_headers[i]:
            record_start_indices.append(i)
        # Find the indices in no_headers which correspond to the start of each arrestee's list of offenses
        elif "Offenses>" in no_headers[i]:
            offenses_start_indices.append(i)
    return record_start_indices, offenses_start_indices

# Create a list of lists, with each sub-list being a single arrest report
def create_list_of_lists(no_headers, record_start_indices):
    records_separated = []
    for i in range(len(record_start_indices)):
        record_list = []
        # If we're at the final record, we need to avoid an IndexError from trying to access index i+1
        if i == len(record_start_indices)-1:
            for j in range(record_start_indices[i],len(no_headers)-1):
                record_list.append(no_headers[j])
        else:
            for j in range(record_start_indices[i], record_start_indices[i+1]):
                record_list.append(no_headers[j])
        records_separated.append(record_list)
    return records_separated

# This function cleans a single arrest record by outputting a dictionary describing each of its key fields
def clean_record(record):
    record_dict = dict.fromkeys(['Arrest','Arrest. ID','Reported','Status','Approved',\
    'Juvenile','Released (S=Summons)','Arrest Date/Time','Zone','Location','Offenses','Offense Codes','Offense Descriptions','Suspect Name','Suspect DOB','Suspect Address'])
    # Record the background info for this incident, including dealing with the extra "($Loss)" column that appears in some reports
    if "($Loss)" in record[0]:
        background_info = record[1].split()[:-1]
    else:
        background_info = record[1].split()
    record_dict['Arrest'] = background_info[0]
    # Leave Assisting Officer ID and Detective ID alone for now, since I'm not 100% I can get those from the split record
    record_dict['Arrest. ID'] = background_info[1]
    # record_dict['Ast. ID'] = ''
    # record_dict['Det. ID'] = ''
    record_dict['Reported'] = background_info[-5]
    record_dict['Status'] = background_info[-4]
    record_dict['Approved'] = background_info[-3]
    record_dict['Juvenile'] = background_info[-2]
    record_dict['Released (S=Summons)'] = background_info[-1]
    # Record the arrest date
    record_dict['Arrest Date/Time'] = record[2].split()[-3] + record[2].split()[-1]
    # Record the "Zone" where the arrest happened
    if 'Zone' in record[3]:
        zone_start_index = record[3].find(record[3].split()[2])
        record_dict['Zone'] = record[3][zone_start_index:]
    elif 'Zone' in record[4]:
        zone_start_index = record[4].find(record[4].split()[1])
        record_dict['Zone'] = record[4][zone_start_index:]
    # Record the location -- this can be either one line in the record or two
    if 'Offenses' in record[6]:
        record_dict['Location'] = record[4] + ', ' + record[5]
    elif 'Offenses' in record[5]:
        record_dict['Location'] = record[4]
    elif 'Offenses' in record[7]:
        record_dict['Location'] = record[5] + ', ' + record[6]
    # Record the offenses committed
    # First, find the line where the offenses start, as well as the line where the suspect info starts
    offenses_start_index = -1
    suspects_start_index = -1
    for i in range(len(record)):
        if 'Suspects' in record[i]:
            suspects_start_index = i
        if 'Offenses' in record[i]:
            offenses_start_index = i
    offenses_string = ''
    offense_codes_string = ''
    offense_descriptions_string = ''
    # Then, collect the info from the offenses one at a time
    for i in range(offenses_start_index, suspects_start_index, 2):
        # If this is the very first offense in the list, we have to remove some extra characters in the first line
        if i == offenses_start_index:
            # If this is the last offense, we should avoid adding the semicolon delimiters to each string
            if i == suspects_start_index - 2:
                # This line cuts off the extra characters at the start of the offense name
                offenses_string += record[i][record[i].find(record[i].split()[2]):]
                offense_codes_string += record[i+1].split()[1]
                if 'IBR' in record[i+1]:
                    offense_descriptions_string += record[i+1].split(' - ')[1]
                # If there's no added description of the offense, we have to leave its Offense Description field empty
                else:
                    offense_descriptions_string += ''
            else:
                offenses_string += record[i][record[i].find(record[i].split()[2]):] + ';'
                offense_codes_string += record[i+1].split()[1] + ';'
                if 'IBR' in record[i+1]:
                    offense_descriptions_string += record[i+1].split(' - ')[1] + ';'
                else:
                    offense_descriptions_string += ';'
        
        else:
            # If this is the last offense, we should avoid adding the semicolon delimiters to each string
            if i == suspects_start_index - 2:
                offenses_string += record[i][record[i].find(record[i].split()[1]):]
                offense_codes_string += record[i+1].split()[1]
                if 'IBR' in record[i+1]:
                    offense_descriptions_string += record[i+1].split(' - ')[1]
                else:
                    offense_descriptions_string += ''
            else:
                offenses_string += record[i][4:] + ';'
                offense_codes_string += record[i+1].split()[1] + ';'
                if 'IBR' in record[i+1]:
                    offense_descriptions_string += record[i+1].split(' - ')[1] + ';'
                else:
                    offense_descriptions_string += ';'
    
    record_dict['Offenses'] = offenses_string
    record_dict['Offense Codes'] = offense_codes_string
    record_dict['Offense Descriptions'] = offense_descriptions_string
    # We need to find the indices at which the suspect's name starts and ends, so that
    # we can grab exactly the characters we need
    suspect_name_start = record[suspects_start_index].find(")")+2
    suspect_name_end = record[suspects_start_index].find("DOB")
    suspect_name = record[suspects_start_index][suspect_name_start:suspect_name_end].strip()
    record_dict['Suspect Name'] = suspect_name.strip()
    record_dict['Suspect DOB'] = record[suspects_start_index][-10:]
    # Deal with one-line vs. two-line vs. nonexistent addresses properly
    if 'Suspects' in record[-3]:
        record_dict['Suspect Address'] = record[-2] + ', ' + record[-1]
    elif 'Suspects' in record[-2]:
        record_dict['Suspect Address'] = record[-1]
    elif 'Suspects' in record[-1]:
        record_dict['Suspect Address'] = ''
    return record_dict

# Prepare the full DataFrame with one week's arrests
def one_week_as_dataframe(records_separated):
    output_df = pd.DataFrame(columns=['Arrest','Arrest. ID','Reported','Status',\
    'Approved','Juvenile','Released (S=Summons)','Arrest Date/Time','Zone','Location',\
    'Offenses','Offense Codes','Offense Descriptions','Suspect Name','Suspect DOB','Suspect Address'])
    for i in range(len(records_separated)):
        single_record = records_separated[i]
        single_record_dict = clean_record(single_record)
        single_record_df = pd.DataFrame(single_record_dict,index=[i])
        output_df = output_df.append(single_record_df)
    # Convert the date reported, arrest date/time, and suspect date of birth to proper datetime format
    output_df['Arrest Date/Time'] = output_df['Arrest Date/Time'].apply(lambda x: pd.to_datetime(x[6:10] + '-' + x[0:2] + '-' \
        + x[3:5] + ' ' + x[-4:]))
    output_df['Reported'] = output_df['Reported'].apply(lambda x: pd.to_datetime(x[6:10] + '-' + x[0:2] + '-' + x[3:5]))
    output_df['Suspect DOB'] = output_df['Suspect DOB'].apply(lambda x: pd.to_datetime(x[6:10] + '-' + x[0:2] + '-' + x[3:5]))
    # Add in an extra column for computing the age of the suspect at the time of the arrest, which we need for merging with NIBRS data
    def calc_age_in_years(date, dob):
        years_diff = date.year - dob.year
        if date.month < dob.month or (date.month == dob.month and date.day < dob.day):
            years_diff -= 1
        return years_diff
    output_df['Suspect Age on Date of Arrest'] = output_df.apply(lambda x: calc_age_in_years(x['Arrest Date/Time'],x['Suspect DOB']),axis=1)
    return output_df

# Set up an empty dataframe to hold the final output
final_df = pd.DataFrame(columns=['Arrest','Arrest. ID',\
'Reported','Status','Approved','Juvenile','Released (S=Summons)','Arrest Date/Time',\
'Zone','Location','Offenses','Offense Codes','Offense Descriptions','Suspect Name','Suspect DOB',\
'Suspect Address','Suspect Age on Date of Arrest'])

# PART 2: DOWNLOAD ALL REPORTS FROM THE SPRINGFIELD WEBSITE

# Choose the name of the (empty) folder where you want to put the reports when they're downloaded
# The folder name should include a forward slash at the end of it
reports_location = '/Users/Alex/Desktop/Download Springfield Logs/'

# Create a list of days on which arrest reports are released (every Saturday)
report_dates = []
report_date = pd.Timestamp('2017-01-07')
todays_date = pd.to_datetime('today')
# Stop listing out report dates when we get to the current time
while str(todays_date)[0:10] > str(report_date)[0:10]:
    report_dates.append(str(report_date)[0:10].replace('-','_'))
    report_date = report_date + pd.DateOffset(days=7)

# This function grabs one report from the Springfield website (based on the report date) and saves it
# The date should be passed in as a string
def get_one_report(date):
    url_start = 'https://www.springfield-ma.gov/police/fileadmin/Police_Dept_files/arrest_logs/'
    url = url_start + date[0:4] + '/arrestlog_' + date + '.pdf'
    # The springfield-ma.gov website's certificate is expired, so I have to set verify=False when accessing the URL,
    # which is kind of dangerous
    pdf = requests.get(url,verify=False)
    # The first part of this should be changed to wherever you want to save these reports
    file_loc = reports_location + 'arrestlog_' + date + '.pdf'
    open_file_for_writing = open(file_loc, 'wb')
    for chunk in pdf.iter_content(100000):
        open_file_for_writing.write(chunk)
    open_file_for_writing.close()

# This for loop will retrieve all existing reports from the Springfield website, then store them in a folder on my desktop
for date in report_dates:
    get_one_report(date)
    print('retrieved and saved report from ' + date)

# PART 3: USING THE NEWLY DOWNLOADED FILES, BUILD THE OUTPUT CSV AND SAVE IT

# Get the names of all reports, then sort them by date
arrest_log_names = os.listdir(reports_location)
# I need to drop certain reports which are stored as images rather than text-based PDFs, since my
# system can't deal with them
arrest_log_names.remove('arrestlog_2017_04_29.pdf')
arrest_log_names.remove('arrestlog_2017_08_05.pdf')
arrest_log_names.remove('arrestlog_2017_08_12.pdf')
# Sort the list of filenames by date
arrest_log_names.sort()

# Iterate through the reports to build one giant dataframe containing all arrest records
for file in arrest_log_names:
    parsed = parser.from_file(reports_location + file)
    lines = get_text_from_tika(parsed)
    no_headers = clean_top_bottom(lines)
    record_start_indices, offenses_start_indices = get_record_and_offenses_indices(no_headers)
    records_separated = create_list_of_lists(no_headers, record_start_indices)
    one_week_df = one_week_as_dataframe(records_separated)
    final_df = final_df.append(one_week_df)
    print('successfully appended dataframe for ' + file)

# Some arrests seem to be listed on two consecutive weeks' reports, so we need to drop the duplicate records
# based on the Arrest (unique identifier) column
final_df.drop_duplicates(subset='Arrest',inplace=True)

# You can specify a particular folder to put the CSV into; by default, it'll be whatever folder this .py file is in
output_location = '/Users/Alex/Desktop/Download Springfield Logs/'

# Save one copy as a pickled file to be easily retrieved in Python for future analysis
# This step can be skipped if you only need the CSV
final_df.to_pickle(output_location + 'springfield_arrest_logs')

# Save another copy as a CSV for more general use
final_df.to_csv(output_location + 'springfield_arrest_logs.csv',index=False)
