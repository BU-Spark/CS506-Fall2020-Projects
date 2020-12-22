import processData
import numpy as np


# read data
district_housing = processData.import_csv('data\\district_housing.csv')
ct_housing = processData.import_csv('data\\ct_housing.csv')
district_shi = processData.import_csv('data\\district_shi.csv')
ct_shi = processData.import_csv('data\\ct_shi.csv')
# add a column to ct_housing and district_housing of percentage of shi units
ct_value = ct_shi.values
district_value = district_shi.values
ct_list = ct_value[:, 0].tolist()
district_list = district_value[:, 0].tolist()
ct_housing_list = ct_housing.values.tolist()
district_housing_list = district_housing.values.tolist()
for i in district_housing_list:
    index = district_list.index(i[0])
    i.append(district_value[index][3])
for i in ct_housing_list:
    index = ct_list.index(i[0])
    i.append(ct_value[index][4])
# write back to file
X_district = np.array(district_housing_list)
header_district = district_housing.columns.values.tolist()
header_district.append('percentage_of_shi_units')
X_ct = np.array(ct_housing_list)
header_ct = ct_housing.columns.values.tolist()
header_ct.append('percentage_of_shi_units')
processData.write_csv('data\\district_housing.csv', X_district, header_district)
processData.write_csv('data\\ct_housing.csv', X_ct, header_ct)