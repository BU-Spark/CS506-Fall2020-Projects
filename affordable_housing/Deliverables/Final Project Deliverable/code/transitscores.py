import pandas as pd 

def process_transit_scores(filename):
    parcels = pd.read_csv(filename)

    parcels['numTransitStops']= parcels['numTransitStops'].fillna(0)
    parcels['walkscore']= parcels['walkscore'].fillna(0)

    #rescale transit stops to be on a scale from 0 to 100, estimating a transit stop score
    parcels['transitStopScore'] = parcels['numTransitStops'].apply(lambda x: x/18*100)
    #combine with walkscore to get a Transit Friendly Score
    parcels['TransitFriendlyScore'] = (parcels['transitStopScore'] + parcels['walkscore']) / 2
    
    #sort by vacant and nonvacant   
    vacantparcels = parcels[((parcels['luc_adj_1'] == 973) | (parcels['luc_adj_1'] == 975))].copy()
    nonvacantparcels = parcels[((parcels['luc_adj_1'] != 973) & (parcels['luc_adj_1'] != 975))].copy()
    #sort them by city, and then ordered by transit score
    sorted_transit_vacant = vacantparcels.sort_values(["muni", "TransitFriendlyScore"], ascending = (True, False))
    sorted_transit_nonvacant = nonvacantparcels.sort_values(["muni", "TransitFriendlyScore"], ascending = (True, False))

    sorted_transit_vacant[['parloc_id','muni','TransitFriendlyScore']].to_csv('vacantTransitFriendly' + filename, index = False)
    sorted_transit_nonvacant[['parloc_id','muni','TransitFriendlyScore']].to_csv('nonvacantTransitFriendly' + filename, index = False)

    sorted_transit_vacant.to_csv('vacantTransitFriendlyFull' + filename, index = False)
    sorted_transit_nonvacant.to_csv('nonvacantTransitFriendlyFull' + filename, index = False)

process_transit_scores('Housing_Final.csv')
process_transit_scores('Transportation_Final.csv')