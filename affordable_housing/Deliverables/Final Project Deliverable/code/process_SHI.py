import processData
import numpy as np


# Read from district and communities
dis_com_df = processData.import_csv('data\\dis_com.csv')
dis_com = dis_com_df.values
# Read from communities shi form
com_shi_df = processData.import_csv('SHI_new.csv')
com_shi = com_shi_df.values
# Confine districts and communities
confined_dis_com = []
confined_dis_com.append(dis_com[0])
for i in range(1, len(dis_com)):
    if dis_com[i][0] != dis_com[i-1][0] or dis_com[i][1] != dis_com[i-1][1]:
        confined_dis_com.append(dis_com[i])
confined_dis_com = np.array(confined_dis_com)
# Select districts and communities
districts = confined_dis_com[:, 0]
communities = com_shi[:, 0]
# Transfer to set to remove duplications
dis_set = set(districts)
com_set = set(communities)
# Form a new list without duplications
dis_new = list(dis_set)
# Combine shi data according to districts
dis_shi = []
m = len(dis_set)
for i in range(m):
    dis_shi.append([])
    dis_shi[i].append(0)
    dis_shi[i].append(0)
for i in range(len(dis_com)):
    index1 = communities.tolist().index(dis_com[i][1])
    index0 = dis_new.index(dis_com[i][0])
    dis_shi[index0][0] = dis_shi[index0][0] + com_shi[index1][1]
    dis_shi[index0][1] = dis_shi[index0][1] + com_shi[index1][3]
for i in range(m):
    dis_shi[i].append(round(dis_shi[i][1]/dis_shi[i][0]*100, 2))

shi_district = []
for i in range(m):
    shi_district.append([])
    shi_district[i].append(dis_new[i])
    shi_district[i].append(dis_shi[i][0])
    shi_district[i].append(dis_shi[i][1])
    shi_district[i].append(dis_shi[i][2])

processData.write_csv('district_shi.csv', shi_district, ['District', 'total_units', 'shi_units', '%'])