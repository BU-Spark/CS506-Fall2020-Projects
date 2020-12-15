import processData
import numpy as np

# read data from csv file
X_housing = processData.import_csv('data\\Housing_Final.csv')
# calculate transit score
numMax = np.max(X_housing['numTransitStops'].tolist())
X_housing['TransitScore'] = 0.5 * X_housing['numTransitStops'] / numMax * 100 + 0.5 * X_housing['walkscore']
# calculate available land value
X_housing['available_land_sqft'] = X_housing['lot_areaft'] - X_housing['bldg_area']
# group data by district and city_and_town
X_housing_district = X_housing.pivot_table(index=['District'],
                                           values=['available_land_sqft', 'TransitScore', 'median_hh_income'],
                                           aggfunc=[np.sum, np.mean])
X_housing_district.to_csv('data\\district_housing.csv')
X_housing_ct = X_housing.pivot_table(index=['muni'],
                                     values=['available_land_sqft', 'TransitScore', 'median_hh_income'],
                                     aggfunc=[np.sum, np.mean])
X_housing_ct.to_csv('data\\ct_housing.csv')
