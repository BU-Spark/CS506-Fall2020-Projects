import processData
import numpy as np


# read data
district_non_vacant_transportation = processData.import_csv('data\\district_transportation_non_vacant.csv')
ct_non_vacant_transportation = processData.import_csv('data\\ct_transportation_non_vacant.csv')
district_shi = processData.import_csv('data\\district_shi.csv')
ct_shi = processData.import_csv('data\\ct_shi.csv')
# add a column to ct_vacant_housing and district_vacant_housing of percentage of shi units
ct_value = ct_shi.values
district_value = district_shi.values
ct_list = ct_value[:, 0].tolist()
district_list = district_value[:, 0].tolist()
ct_non_vacant_transportation_list = ct_non_vacant_transportation.values.tolist()
district_non_vacant_transportation_list = district_non_vacant_transportation.values.tolist()
for i in district_non_vacant_transportation_list:
    index = district_list.index(i[0])
    i.append(district_value[index][3])
for i in ct_non_vacant_transportation_list:
    index = ct_list.index(i[0])
    i.append(ct_value[index][4])
# write back to file
X_district = np.array(district_non_vacant_transportation_list)
header_district = district_non_vacant_transportation.columns.values.tolist()
header_district.append('percentage_of_shi_units')
X_ct = np.array(ct_non_vacant_transportation_list)
header_ct = ct_non_vacant_transportation.columns.values.tolist()
header_ct.append('percentage_of_shi_units')
processData.write_csv('data\\district_transportation_non_vacant.csv', X_district, header_district)
processData.write_csv('data\\ct_transportation_non_vacant.csv', X_ct, header_ct)