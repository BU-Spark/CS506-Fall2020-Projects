import processData
import numpy as np


# read data
district_transportation = processData.import_csv('data\\district_transportation.csv')
ct_transportation = processData.import_csv('data\\ct_transportation.csv')
district_shi = processData.import_csv('data\\district_shi.csv')
ct_shi = processData.import_csv('data\\ct_shi.csv')
# add a column to ct_transportation and district_transportation of percentage of shi units
ct_value = ct_shi.values
district_value = district_shi.values
ct_list = ct_value[:, 0].tolist()
district_list = district_value[:, 0].tolist()
ct_transportation_list = ct_transportation.values.tolist()
district_transportation_list = district_transportation.values.tolist()
for i in district_transportation_list:
    index = district_list.index(i[0])
    i.append(district_value[index][3])
for i in ct_transportation_list:
    index = ct_list.index(i[0])
    i.append(ct_value[index][4])
# write back to file
X_district = np.array(district_transportation_list)
header_district = district_transportation.columns.values.tolist()
header_district.append('percentage_of_shi_units')
X_ct = np.array(ct_transportation_list)
header_ct = ct_transportation.columns.values.tolist()
header_ct.append('percentage_of_shi_units')
processData.write_csv('data\\district_transportation.csv', X_district, header_district)
processData.write_csv('data\\ct_transportation.csv', X_ct, header_ct)