# Vibons Team1 - Journey app
# Team member: Lingyan Jiang, Ruoqi Shi, Jiaqi Zhao 

import pandas as pd
import numpy as np

X = pd.read_csv('new_data.csv', parse_dates = True, low_memory = False)
#print(X.shape)
X = X.values

# delete duplicates in device and content_type and prepare for projecting string to number
res_list = X.T.tolist()
b = list(set(res_list[10]))

device = X[:,11]
for i in range(len(device)):
    if device[i] == 'Device':
        print(i)
        
content_type = X[:,6]
for i in range(len(content_type)):
    if content_type[i] == 'Content Type':
        print(i)
#print(X[:,6])

#Mapping device, channel and content_type to number
device = X[:,11]
#print(device)
channel = X[:,12]
#print(channel)
content_type = X[:,6]
#print(content_type)
for i in range(len(device)):
    if device[i] == 'Android':
        device[i] = 4
    elif device[i] == 'iOS':
        device[i] = 3    
    elif device[i] == 'Web':
        device[i] = 2 
    elif device[i] == 'Mobile Web (Tablet)':
        device[i] = 1
    elif device[i] == 'Mobile Web':
        device[i] = 5
    else:
        device[i] = 0
#print(device)

for i in range(len(channel)):
    if channel[i] == 'Mobile Notification':
        channel[i] = 2
    elif channel[i] == 'From Email':
        channel[i] = 1
    elif channel[i] == 'Direct Connection':
        channel[i] = 3
    else:
        channel[i] = 0
#print(channel)

content_type_list = ['KEY_CONTACT_NEWHIRE', 'EXTERNAL_ARTICLE', 'CHECKLIST', 'KNOWLEDGE_REQUIREMENT_NEWHIRE', 'BOOK_SUGGESTION', 'QUIZ', 'KEY_CONTACT_MANAGER', 'EXTERNAL_VIDEO', 'SURVEY', 'MEETING', 'LIVE_EVENT', 'INTERNAL_ARTICLE', 'FLIPBOOK', 'KNOWLEDGE_REQUIREMENT_MANAGER', 'INFOGRAPHIC', 'Content Type', 'INTERNAL_VIDEO', 'QUOTES']

for i in range(len(content_type)):
    if content_type[i] == content_type_list[0]:
        content_type[i] = 17000
    elif content_type[i] == content_type_list[1]:
        content_type[i] = 1000
    elif content_type[i] == content_type_list[2]:
        content_type[i] = 2000
    elif content_type[i] == content_type_list[3]:
        content_type[i] = 3000
    elif content_type[i] == content_type_list[4]:
        content_type[i] = 4000
    elif content_type[i] == content_type_list[5]:
        content_type[i] = 5000
    elif content_type[i] == content_type_list[6]:
        content_type[i] = 6000
    elif content_type[i] == content_type_list[7]:
        content_type[i] = 7000
    elif content_type[i] == content_type_list[8]:
        content_type[i] = 8000
    elif content_type[i] == content_type_list[9]:
        content_type[i] = 9000
    elif content_type[i] == content_type_list[10]:
        content_type[i] = 10000
    elif content_type[i] == content_type_list[11]:
        content_type[i] = 11000
    elif content_type[i] == content_type_list[12]:
        content_type[i] = 12000
    elif content_type[i] == content_type_list[13]:
        content_type[i] = 13000
    elif content_type[i] == content_type_list[14]:
        content_type[i] = 14000
    elif content_type[i] == content_type_list[15]:
        content_type[i] = 15000
    elif content_type[i] == content_type_list[16]:
        content_type[i] = 16000
    else:
        content_type[i] = 0
#print(content_type)

#select the data from cleaned data
clean_data = pd.DataFrame(X)
#print(clean_data.head())
c = clean_data.values
#print(c)

# use mode() function to replace the nan value
max_value = clean_data[11].mode()
clean_data[11] = clean_data[11].replace([0],max_value)
#print(clean_data[11].value_counts())

# use mode() function to replace the nan value
content_max = clean_data[6].mode()
#print(content_max)
#print(clean_data[6].value_counts())
clean_data[6] = clean_data[6].replace([0],content_max)
#print('after: ',clean_data[6].value_counts())

# use mode() function to replace the nan value
max_value = clean_data[12].mode()
clean_data[12] = clean_data[12].replace([0],max_value)
#print(clean_data[12].value_counts())

#drop Flipbook from the user ID
clean_data.drop(clean_data[clean_data[1] == 'FLIPBOOK'].index, inplace = True)

#drop nan value
clean_data.dropna(how = 'any', axis = 0, inplace = True)

#reset index of cleaned data
clean_data.reset_index(inplace=True, drop=True)

#transfer userID index to integer
clean_data[1] = clean_data[1].fillna(0.0).astype('int')

#Replace the Action nan value to 0 and transfer Action type to integer
clean_data[9] = clean_data[9].replace(['nan'],'0')
clean_data[9] = clean_data[9].fillna(0.0).astype('int')

#Replace the Content_Type nan value to [] and transfer Action Content_Type type to string
#clean_data.drop(index = 1789049, axis = 0)
clean_data[5] = clean_data[5].replace(['nan'],"")
clean_data[5] = clean_data[5].astype('str')

#Give the new cleaned data the column title
clean_data.columns = ['Customer Id','User Id', 'User Created At', 'Activation Date', 'Activity Date','Name', 'Content Type', 'Content ID','Journey Name', 'Action', 'Duration','Device', 'Channel', 'Session Id', 'Rating']

#Group by with userID and order by descending

#clean_data = clean_data[:300].groupby(['User Id'],axis=1)
#print(Grouped.size())

clean_data.groupby(['User Id'])

#print(clean_data.groupby(['User Id']).count())

group_label = clean_data.groupby(['User Id']).groups
#print(group_label)

#choose the columns from cleaned data that we need to process later
open_time = pd.DataFrame()
open_time = clean_data.loc[:, ('User Id','Activation Date','Activity Date','Name','Content Type','Action','User Created At')]
#diff = pd.Timestamp(open_time['Activity Date'])- pd.Timestamp(open_time['Activation Date'])
#diff = pd.to_datetime(open_time['Activity Date'])- pd.to_datetime(open_time['Activation Date'])
#print(diff)
#open_time.insert(5, "Time lag", diff)
#print(open_time)
#open_time.dropna(how = "any")

#transfer the Activity Date to date and hour seperately
date = open_time['Activity Date'].map(lambda x: str(x)[0:10])
date = pd.to_datetime(date)
open_time['Activity Day'] = date.dt.day_name()
hr = open_time['Activity Date'].map(lambda x: str(x)[11:13])
open_time['hour'] = hr

# # Action Distribution

#find the action distribution
import collections
actiondis = open_time["Action"].values.tolist()
collections.Counter(actiondis).most_common()


# # Action >= 85

#Find the data when action rate is >= 85
Action85 = open_time[open_time.loc[:,("Action")] >= 85] 
Action = clean_data[["Content Type","Device","Channel","Action"]]

#Mapping the data to number for convenience
def tonum(x):
    """
    take x, activity day as input
    return int Mon -> 100, Tue -> , etc
    """
    if x == "Monday":
        #print("1")
        return 100
    elif x == "Tuesday":
        return 200
    elif x == "Wednesday":
        return 300
    elif x == "Thursday":
        return 400
    elif x == "Friday":
        return 500
    elif x == "Saturday":
        return 600
    else:
        return 700

#transfer the data to number using the function above
day_num = open_time.loc[:,('Activity Day')].map(lambda x: tonum(x))

#store the date into day_num column
Action85["day_num"] = day_num

#transfer the hour to number
hr_num = Action85['hour'].map(lambda x: int(x))

#store the hour into hr_num column
Action85["hour"] = hr_num

#add the hour and day_num together in order for calculating convenience
total_num = Action85['hour'].add(Action85['day_num'])

#store the total_num into total_num column
Action85['total_num'] = total_num

#add the content_type and total_num together in order for calculating convenience
Action85['Content_Type_total'] = ''
content_type_total = Action85['Content Type'].add(Action85['total_num'])
Action85['Content_Type_total'] = content_type_total

#choose the unique UserID
df85 = pd.DataFrame({'User Id':Action85["User Id"].unique()})

#store all total_num of one user into one dataframe space
df85['total_num'] = [list(set(Action85['total_num'].loc[Action85['User Id'] == x['User Id']])) for _, x in df85.iterrows()]

#delete the duplicates UserID
df = Action85.groupby('User Id').agg(lambda x: x.tolist()) 

#store the index which is thw userID into index_df
index_df = df.index.values

#add one column "count_total" in dataframe
df["count_total"] = ''

#create a function for counting same total_num
from collections import Counter
def count(x):
    Counter(df["total_num"][21]).most_common()

#count same total_num of one user and order from largest to smallest
for i in range(len(index_df)):
    df['count_total'][index_df[i]] = Counter(df['total_num'][index_df[i]]).most_common()

#create a function to transfer the count_total number of each user into data and store in the different columns
def sort_arr(arr):
    res = [[],[],[],[],[],[],[]]
    for i in range(len(arr)):
        item = str(arr[i][0])
        if item[0] == "1":
            res[0].append(arr[i])
            #return res
        elif item[0] == "2":
            res[1].append(arr[i])
            #return res
        elif item[0] == "3":
            res[2].append(arr[i])
            #return res
        elif item[0] == "4":
            res[3].append(arr[i])
            #return res
        elif item[0] == "5":
            res[4].append(arr[i])
            #return res
        elif item[0] == "6":
            res[5].append(arr[i])
            #return res
        else:
            res[6].append(arr[i])
            #return res
    return res
import statistics

#in order to find the better user impression, create a function to choose the time which above the average frequency
def get_above(arr):
    freq = []
    for i in range(len(arr)):
        ele = arr[i][-1]
        freq.append(ele)
    
    mean = statistics.mean(freq)
    l = []
    for i in range(len(arr)):
        if arr[i][-1] >= mean:
            l.append(arr[i])
    return l

# create a function to find the frequency of a selected user
def find_freq(arr):
    res = []
    sorted_arr = sort_arr(arr)
    for i in range(len(sorted_arr)):
        if len(sorted_arr[i]) == 0:
            res.append([])
        else:
            if len(sorted_arr[i]) == 1:
                res.append(sorted_arr[i])
            else:
                subarr = sorted_arr[i]
                freq = []
                for i in range(len(arr)):
                    ele = arr[i][-1]
                    freq.append(ele)
                l = []
                mean = statistics.mean(freq)
                for j in range(len(subarr)):
                    if subarr[j][-1] >= mean:
                        l.append(subarr[j])
                res.append(l)
    return res
    
#create a new column in dataframe
df["every_day_freq"] = ''

#find a frequency for each user
for i in range(len(index_df)):
    arr = df["count_total"][index_df[i]]
    df["every_day_freq"][index_df[i]] = find_freq(arr)

#create new columns to dataframe
df['Mon'] = ''
df['Tue'] = ''
df['Wed'] = ''
df['Thu'] = ''
df['Fri'] = ''
df['Sat'] = ''
df['Sun'] = ''

#generate hour with corresponding frequency on each day of one week
for i in range(len(index_df)):
    arr = df["every_day_freq"][index_df[i]]
    temp = []
    ### Monday
    if len(arr[0]) == 0:
        df['Mon'][index_df[i]] = [np.nan]
    else:
        if len(arr[0]) == 1:
            df['Mon'][index_df[i]] = [[arr[0][0][0]%100, arr[0][0][1]]]
        else:
            temp = []
            for j in range(len(arr[0])):
                ele = [arr[0][j][0]%100, arr[0][j][1]]
                temp.append(ele)
                
            df['Mon'][index_df[i]] = temp
    ### Tuesday
    if len(arr[1]) == 0:
        df['Tue'][index_df[i]] = [np.nan]
    else:
        if len(arr[1]) == 1:
            df['Tue'][index_df[i]] = [[arr[1][0][0]%100, arr[1][0][1]]]
        else:
            temp = []
            for j in range(len(arr[1])):
                ele = [arr[1][j][0]%100, arr[1][j][1]]
                temp.append(ele)
            df['Tue'][index_df[i]] = temp
    ### Wednesday
    if len(arr[2]) == 0:
        df['Wed'][index_df[i]] = [np.nan]
    else:
        if len(arr[2]) == 1:
            df['Wed'][index_df[i]] = [[arr[2][0][0]%100, arr[2][0][1]]]
        else:
            temp = []
            for j in range(len(arr[2])):
                ele = [arr[2][j][0]%100, arr[2][j][1]]
                temp.append(ele)
            df['Wed'][index_df[i]] = temp
    ### Thursday
    if len(arr[3]) == 0:
        df['Thu'][index_df[i]] = [np.nan]
    else:
        if len(arr[3]) == 1:
            df['Thu'][index_df[i]] = [[arr[3][0][0]%100, arr[3][0][1]]]
        else:
            temp = []
            for j in range(len(arr[3])):
                ele = [arr[3][j][0]%100, arr[3][j][1]]
                temp.append(ele)
            df['Thu'][index_df[i]] = temp
    ### Friday
    if len(arr[4]) == 0:
        df['Fri'][index_df[i]] = [np.nan]
    else:
        if len(arr[4]) == 1:
            df['Fri'][index_df[i]] = [[arr[4][0][0]%100, arr[4][0][1]]]
        else:
            temp = []
            for j in range(len(arr[4])):
                ele = [arr[4][j][0]%100, arr[4][j][1]]
                temp.append(ele)
            df['Fri'][index_df[i]] = temp
    ### Saturday
    if len(arr[5]) == 0:
        df['Sat'][index_df[i]] = [np.nan]
    else:
        if len(arr[5]) == 1:
            df['Sat'][index_df[i]] = [[arr[5][0][0]%100, arr[5][0][1]]]
        else:
            temp = []
            for j in range(len(arr[5])):
                ele = [arr[5][j][0]%100, arr[5][j][1]]
                temp.append(ele)
            df['Sat'][index_df[i]] = temp
    ### Sunday
    if len(arr[6]) == 0:
        df['Sun'][index_df[i]] = [np.nan]
    else:
        if len(arr[6]) == 1:
            df['Sun'][index_df[i]] = [[arr[6][0][0]%100, arr[6][0][1]]]
        else:
            temp = []
            for j in range(len(arr[6])):
                ele = [arr[6][j][0]%100, arr[6][j][1]]
                temp.append(ele)
            df['Sun'][index_df[i]] = temp

#convert userID into index
for i in range(len(index_df)):
    df['Content_Type_total'][index_df[i]] = list(set(df['Content_Type_total'][index_df[i]]))

#create a function to find the nth_digit of one number
def nth_digit(number, digit):
    return abs(number) // (10**(digit-1)) % 10

#add Content_Type into each space in the dataframe after hour and frequency
#Monday
for i in range(len(index_df)):
    if df['Mon'][index_df[i]] == [np.nan]:
        pass
    else:
        for j in range(len(df['Mon'][index_df[i]])):
            for n in range(len(df['Content_Type_total'][index_df[i]])):
                if nth_digit(df['Content_Type_total'][index_df[i]][n],3) == 1 and df['Mon'][index_df[i]][j][0] == df['Content_Type_total'][index_df[i]][n] % 100:
                    df['Mon'][index_df[i]][j].append(df['Content_Type_total'][index_df[i]][n] // 1000)   
        
#Tuesday
for i in range(len(index_df)):
    if df['Tue'][index_df[i]] == [np.nan]:
        pass
    else:
        for j in range(len(df['Tue'][index_df[i]])):
            for n in range(len(df['Content_Type_total'][index_df[i]])):
                if nth_digit(df['Content_Type_total'][index_df[i]][n],3) == 2 and df['Tue'][index_df[i]][j][0] == df['Content_Type_total'][index_df[i]][n] % 100:
                    df['Tue'][index_df[i]][j].append(df['Content_Type_total'][index_df[i]][n] // 1000)
        
#Wednesday
for i in range(len(index_df)):
    if df['Wed'][index_df[i]] == [np.nan]:
        pass
    else:
        for j in range(len(df['Wed'][index_df[i]])):
            for n in range(len(df['Content_Type_total'][index_df[i]])):
                if nth_digit(df['Content_Type_total'][index_df[i]][n],3) == 3 and df['Wed'][index_df[i]][j][0] == df['Content_Type_total'][index_df[i]][n] % 100:
                    df['Wed'][index_df[i]][j].append(df['Content_Type_total'][index_df[i]][n] // 1000)
        
#Thursday
for i in range(len(index_df)):
    if df['Thu'][index_df[i]] == [np.nan]:
        pass
    else:
        for j in range(len(df['Thu'][index_df[i]])):
            for n in range(len(df['Content_Type_total'][index_df[i]])):
                if nth_digit(df['Content_Type_total'][index_df[i]][n],3) == 4 and df['Thu'][index_df[i]][j][0] == df['Content_Type_total'][index_df[i]][n] % 100:
                    df['Thu'][index_df[i]][j].append(df['Content_Type_total'][index_df[i]][n] // 1000)
        
#Friday
for i in range(len(index_df)):
    if df['Fri'][index_df[i]] == [np.nan]:
        pass
    else:
        for j in range(len(df['Fri'][index_df[i]])):
            for n in range(len(df['Content_Type_total'][index_df[i]])):
                if nth_digit(df['Content_Type_total'][index_df[i]][n],3) == 5 and df['Fri'][index_df[i]][j][0] == df['Content_Type_total'][index_df[i]][n] % 100:
                    df['Fri'][index_df[i]][j].append(df['Content_Type_total'][index_df[i]][n] // 1000)
        
#Saturday
for i in range(len(index_df)):
    if df['Sat'][index_df[i]] == [np.nan]:
        pass
    else:
        for j in range(len(df['Sat'][index_df[i]])):
            for n in range(len(df['Content_Type_total'][index_df[i]])):
                if nth_digit(df['Content_Type_total'][index_df[i]][n],3) == 6 and df['Sat'][index_df[i]][j][0] == df['Content_Type_total'][index_df[i]][n] % 100:
                    df['Sat'][index_df[i]][j].append(df['Content_Type_total'][index_df[i]][n] // 1000)
        
#Sunday
for i in range(len(index_df)):
    if df['Sun'][index_df[i]] == [np.nan]:
        pass
    else:
        for j in range(len(df['Sun'][index_df[i]])):
            for n in range(len(df['Content_Type_total'][index_df[i]])):
                if nth_digit(df['Content_Type_total'][index_df[i]][n],3) == 7 and df['Sun'][index_df[i]][j][0] == df['Content_Type_total'][index_df[i]][n] % 100:
                    df['Sun'][index_df[i]][j].append(df['Content_Type_total'][index_df[i]][n] // 1000)

#Final result
customer85_100 = pd.DataFrame()
customer85_100 = df.loc[:,('Mon','Tue','Wed','Thu','Fri','Sat','Sun')]

#Final result store in csv file
customer85_100.to_csv('customer85_100_1206.csv')

# # Action > 0 and Action < 85

# **Same steps and functions as action >= 85**

Action0_85 = open_time[(open_time.loc[:,("Action")] < 85) & (open_time.loc[:,("Action")] > 0)]
Action = clean_data[["Content Type","Content ID","Device","Channel","Action"]]
Action.isna().sum()
Action["Content ID"] = Action["Content ID"].astype("int")
day_num = open_time.loc[:,('Activity Day')].map(lambda x: tonum(x))
Action0_85["day_num"] = day_num
hr_num = Action0_85['hour'].map(lambda x: int(x))
Action0_85["hour"] = hr_num
total_num = Action0_85['hour'].add(Action0_85['day_num'])
Action0_85['total_num'] = total_num
df0_85 = pd.DataFrame({'User Id':Action0_85["User Id"].unique()})
df0_85['total_num'] = [list(set(Action0_85['total_num'].loc[Action0_85['User Id'] == x['User Id']])) for _, x in df0_85.iterrows()]
df0_85_res = Action0_85.groupby('User Id').agg(lambda x: x.tolist())
index_df0_85_res = df0_85_res.index.values
df0_85_res["count_total"] = ''
for i in range(len(index_df0_85_res)):
    df0_85_res['count_total'][index_df0_85_res[i]] = Counter(df0_85_res['total_num'][index_df0_85_res[i]]).most_common()
df0_85_res["every_day_freq"] = ''
for i in range(len(index_df0_85_res)):
    arr = df0_85_res["count_total"][index_df0_85_res[i]]
    df0_85_res["every_day_freq"][index_df0_85_res[i]] = find_freq(arr)
df0_85_res.head()
df0_85_res['Mon'] = ''
df0_85_res['Tue'] = ''
df0_85_res['Wed'] = ''
df0_85_res['Thu'] = ''
df0_85_res['Fri'] = ''
df0_85_res['Sat'] = ''
df0_85_res['Sun'] = ''

for i in range(len(index_df0_85_res)):
    arr = df0_85_res["every_day_freq"][index_df0_85_res[i]]
    temp = []
    ### Monday
    if len(arr[0]) == 0:
        df0_85_res['Mon'][index_df0_85_res[i]] = [np.nan]
    else:
        if len(arr[0]) == 1:
            df0_85_res['Mon'][index_df0_85_res[i]] = [arr[0][0][0]%100, arr[0][0][1]]
        else:
            temp = []
            for j in range(len(arr[0])):
                ele = [arr[0][j][0]%100, arr[0][j][1]]
                temp.append(ele)
                
            df0_85_res['Mon'][index_df0_85_res[i]] = temp
    ### Tuesday
    if len(arr[1]) == 0:
        df0_85_res['Tue'][index_df0_85_res[i]] = [np.nan]
    else:
        if len(arr[1]) == 1:
            df0_85_res['Tue'][index_df0_85_res[i]] = [arr[1][0][0]%100, arr[1][0][1]]
        else:
            temp = []
            for j in range(len(arr[1])):
                ele = [arr[1][j][0]%100, arr[1][j][1]]
                temp.append(ele)
            df0_85_res['Tue'][index_df0_85_res[i]] = temp
    ### Wednesday
    if len(arr[2]) == 0:
        df0_85_res['Wed'][index_df0_85_res[i]] = [np.nan]
    else:
        if len(arr[2]) == 1:
            df0_85_res['Wed'][index_df0_85_res[i]] = [arr[2][0][0]%100, arr[2][0][1]]
        else:
            temp = []
            for j in range(len(arr[2])):
                ele = [arr[2][j][0]%100, arr[2][j][1]]
                temp.append(ele)
            df0_85_res['Wed'][index_df0_85_res[i]] = temp
    ### Thursday
    if len(arr[3]) == 0:
        df0_85_res['Thu'][index_df0_85_res[i]] = [np.nan]
    else:
        if len(arr[3]) == 1:
            df0_85_res['Thu'][index_df0_85_res[i]] = [arr[3][0][0]%100, arr[3][0][1]]
        else:
            temp = []
            for j in range(len(arr[3])):
                ele = [arr[3][j][0]%100, arr[3][j][1]]
                temp.append(ele)
            df0_85_res['Thu'][index_df0_85_res[i]] = temp
    ### Friday
    if len(arr[4]) == 0:
        df0_85_res['Fri'][index_df0_85_res[i]] = [np.nan]
    else:
        if len(arr[4]) == 1:
            df0_85_res['Fri'][index_df0_85_res[i]] = [arr[4][0][0]%100, arr[4][0][1]]
        else:
            temp = []
            for j in range(len(arr[4])):
                ele = [arr[4][j][0]%100, arr[4][j][1]]
                temp.append(ele)
            df0_85_res['Fri'][index_df0_85_res[i]] = temp
    ### Saturday
    if len(arr[5]) == 0:
        df0_85_res['Sat'][index_df0_85_res[i]] = [np.nan]
    else:
        if len(arr[5]) == 1:
            df0_85_res['Sat'][index_df0_85_res[i]] = [arr[5][0][0]%100, arr[5][0][1]]
        else:
            temp = []
            for j in range(len(arr[5])):
                ele = [arr[5][j][0]%100, arr[5][j][1]]
                temp.append(ele)
            df0_85_res['Sat'][index_df0_85_res[i]] = temp
    ### Sunday
    if len(arr[6]) == 0:
        df0_85_res['Sun'][index_df0_85_res[i]] = [np.nan]
    else:
        if len(arr[6]) == 1:
            df0_85_res['Sun'][index_df0_85_res[i]] = [arr[6][0][0]%100, arr[6][0][1]]
        else:
            temp = []
            for j in range(len(arr[6])):
                ele = [arr[6][j][0]%100, arr[6][j][1]]
                temp.append(ele)
            df0_85_res['Sun'][index_df0_85_res[i]] = temp

customer0_85 = df0_85_res.loc[:,('Mon','Tue','Wed','Thu','Fri','Sat','Sun')]
#customer0_85.head()

# # Delete duplicated user id from Action 85-100

customer0_85_deleted = customer0_85.loc[customer0_85.index.difference(customer85_100.index), ]

customer0_85_deleted.to_csv('customer0_85_deleted.csv')

# # Action == 0

# **Same steps and functions as Action >= 85**

Action0 = open_time[(open_time.loc[:,("Action")] == 0)]
Action = clean_data[["Content Type","Content ID","Device","Channel","Action"]]
Action.isna().sum()
Action["Content ID"] = Action["Content ID"].astype("int")
day_num = open_time.loc[:,('Activity Day')].map(lambda x: tonum(x))
Action0["day_num"] = day_num
hr_num = Action0['hour'].map(lambda x: int(x))
Action0["hour"] = hr_num
total_num = Action0['hour'].add(Action0['day_num'])
Action0['total_num'] = total_num
df0 = pd.DataFrame({'User Id':Action0["User Id"].unique()})
df0['total_num'] = [list(set(Action0['total_num'].loc[Action0['User Id'] == x['User Id']])) for _, x in df0.iterrows()]
df0_res = Action0.groupby('User Id').agg(lambda x: x.tolist())
index_df0_res = df0_res.index.values
df0_res["count_total"] = ''
for i in range(len(index_df0_res)):
    df0_res['count_total'][index_df0_res[i]] = Counter(df0_res['total_num'][index_df0_res[i]]).most_common()
df0_res["every_day_freq"] = ''
for i in range(len(index_df0_res)):
    arr = df0_res["count_total"][index_df0_res[i]]
    df0_res["every_day_freq"][index_df0_res[i]] = find_freq(arr)
df0_res.head()
df0_res['Mon'] = ''
df0_res['Tue'] = ''
df0_res['Wed'] = ''
df0_res['Thu'] = ''
df0_res['Fri'] = ''
df0_res['Sat'] = ''
df0_res['Sun'] = ''

for i in range(len(index_df0_res)):
    arr = df0_res["every_day_freq"][index_df0_res[i]]
    temp = []
    ### Monday
    if len(arr[0]) == 0:
        df0_res['Mon'][index_df0_res[i]] = [np.nan]
    else:
        if len(arr[0]) == 1:
            df0_res['Mon'][index_df0_res[i]] = [arr[0][0][0]%100, arr[0][0][1]]
        else:
            temp = []
            for j in range(len(arr[0])):
                ele = [arr[0][j][0]%100, arr[0][j][1]]
                temp.append(ele)
                
            df0_res['Mon'][index_df0_res[i]] = temp
    ### Tuesday
    if len(arr[1]) == 0:
        df0_res['Tue'][index_df0_res[i]] = [np.nan]
    else:
        if len(arr[1]) == 1:
            df0_res['Tue'][index_df0_res[i]] = [arr[1][0][0]%100, arr[1][0][1]]
        else:
            temp = []
            for j in range(len(arr[1])):
                ele = [arr[1][j][0]%100, arr[1][j][1]]
                temp.append(ele)
            df0_res['Tue'][index_df0_res[i]] = temp
    ### Wednesday
    if len(arr[2]) == 0:
        df0_res['Wed'][index_df0_res[i]] = [np.nan]
    else:
        if len(arr[2]) == 1:
            df0_res['Wed'][index_df0_res[i]] = [arr[2][0][0]%100, arr[2][0][1]]
        else:
            temp = []
            for j in range(len(arr[2])):
                ele = [arr[2][j][0]%100, arr[2][j][1]]
                temp.append(ele)
            df0_res['Wed'][index_df0_res[i]] = temp
    ### Thursday
    if len(arr[3]) == 0:
        df0_res['Thu'][index_df0_res[i]] = [np.nan]
    else:
        if len(arr[3]) == 1:
            df0_res['Thu'][index_df0_res[i]] = [arr[3][0][0]%100, arr[3][0][1]]
        else:
            temp = []
            for j in range(len(arr[3])):
                ele = [arr[3][j][0]%100, arr[3][j][1]]
                temp.append(ele)
            df0_res['Thu'][index_df0_res[i]] = temp
    ### Friday
    if len(arr[4]) == 0:
        df0_res['Fri'][index_df0_res[i]] = [np.nan]
    else:
        if len(arr[4]) == 1:
            df0_res['Fri'][index_df0_res[i]] = [arr[4][0][0]%100, arr[4][0][1]]
        else:
            temp = []
            for j in range(len(arr[4])):
                ele = [arr[4][j][0]%100, arr[4][j][1]]
                temp.append(ele)
            df0_res['Fri'][index_df0_res[i]] = temp
    ### Saturday
    if len(arr[5]) == 0:
        df0_res['Sat'][index_df0_res[i]] = [np.nan]
    else:
        if len(arr[5]) == 1:
            df0_res['Sat'][index_df0_res[i]] = [arr[5][0][0]%100, arr[5][0][1]]
        else:
            temp = []
            for j in range(len(arr[5])):
                ele = [arr[5][j][0]%100, arr[5][j][1]]
                temp.append(ele)
            df0_res['Sat'][index_df0_res[i]] = temp
    ### Sunday
    if len(arr[6]) == 0:
        df0_res['Sun'][index_df0_res[i]] = [np.nan]
    else:
        if len(arr[6]) == 1:
            df0_res['Sun'][index_df0_res[i]] = [arr[6][0][0]%100, arr[6][0][1]]
        else:
            temp = []
            for j in range(len(arr[6])):
                ele = [arr[6][j][0]%100, arr[6][j][1]]
                temp.append(ele)
            df0_res['Sun'][index_df0_res[i]] = temp

customer0 = df0_res.loc[:,('Mon','Tue','Wed','Thu','Fri','Sat','Sun')]
#customer0.head()

customer0.to_csv('customer0.csv')
customer0_85.to_csv('customer0_85.csv')
customer85_100.to_csv('customer85_100.csv')



