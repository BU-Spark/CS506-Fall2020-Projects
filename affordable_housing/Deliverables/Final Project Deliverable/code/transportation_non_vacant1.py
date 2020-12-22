import processData
import numpy as np
import analysis

# read data from csv file
X_transportation = processData.import_csv('data\\Transportation_Final.csv')
# calculate transit score
numMax = np.max(X_transportation['numTransitStops'].tolist())
X_transportation['TransitScore'] = 0.5 * X_transportation['numTransitStops'] / numMax * 100 + 0.5 * X_transportation[
    'walkscore']
# calculate available land value
X_transportation['available_land_sqft'] = X_transportation['lot_areaft'] - X_transportation['bldg_area']
# filter none_vacant land parcels
X_transportation_non_vacant = analysis.filter_luc(X_transportation, 'transportation_non_vacant')
# group data by district and city_and_town
X_transportation_non_vacant_district = X_transportation_non_vacant.pivot_table(index=['District'],
                                                                               values=['available_land_sqft',
                                                                                       'TransitScore',
                                                                                       'median_hh_income'],
                                                                               aggfunc=[np.sum, np.mean])
X_transportation_non_vacant_district.to_csv('data\\district_transportation_non_vacant.csv')
X_transportation_non_vacant_ct = X_transportation_non_vacant.pivot_table(index=['muni'],
                                                                         values=['available_land_sqft', 'TransitScore',
                                                                                 'median_hh_income'],
                                                                         aggfunc=[np.sum, np.mean])
X_transportation_non_vacant_ct.to_csv('data\\ct_transportation_non_vacant.csv')
