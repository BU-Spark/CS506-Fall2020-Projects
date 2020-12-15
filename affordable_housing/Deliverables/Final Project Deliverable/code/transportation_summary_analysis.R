
#R packages
library(tidyverse)

##Read in the transportation file
Transportation <- read.csv("/Users/reinachau/Documents/Spark Project/transportation.csv", stringsAsFactors=FALSE) %>%
  select(index, mapc_id, luc_adj_1, luc_adj_2, muni_id, muni, District, lot_areaft, bldg_area, numTransitStops, median_hh_income, addr_num, addr_str, owner_city, owner_stat, owner_zip)

##Read in the walk score file
Transportation_WalkScore_TransitScore <- read.csv("/Users/reinachau/Documents/Spark Project/Transportation_WalkScore_TransitScore.csv", stringsAsFactors=FALSE) %>% 
  select(index, mapc_id, latitude, longitude, walkscore, transitscore, transit_score_description, transit_score_summary)

#Join the walk score with transportation data
Transportation_WalkScore_TransitScore <- Transportation %>% left_join(Transportation_WalkScore_TransitScore)

#Read in the transportation estimate and merged the previous merged data
Transportation_Estimate <- read.csv("/Users/reinachau/Documents/Spark Project/Transportation_Estimate.csv", stringsAsFactors=FALSE) %>% 
  left_join(
    read.csv("/Users/reinachau/Documents/Spark Project/transportation.csv", stringsAsFactors=FALSE) %>%
      select(index, mapc_id, land_value, bldg_value, othr_value, total_value)
  ) %>% 
  mutate(
    land_value=ifelse(match_parcel_id==TRUE, assessed_land_value, land_value),
    bldg_value=ifelse(match_parcel_id==TRUE, assessed_building_value, bldg_value),
    othr_value=ifelse(match_parcel_id==TRUE, total_assessed_value - (assessed_land_value+assessed_building_value), othr_value),
    total_value=ifelse(match_parcel_id==TRUE, total_assessed_value, total_value)
  ) %>% 
  select(index, mapc_id, parloc_id, land_value, bldg_value, othr_value, total_value)

#Create the final combined file
Transportation_Estimate_Final <- Transportation_Estimate %>% 
  left_join(Transportation_WalkScore_TransitScore)  %>% 
  select(index, mapc_id, parloc_id, luc_adj_1, luc_adj_2, muni_id, muni, District, land_value, bldg_value, othr_value, total_value, lot_areaft, bldg_area, addr_num, addr_str, owner_city, owner_stat, owner_zip, median_hh_income, latitude, longitude, numTransitStops, walkscore, transitscore, transit_score_description, transit_score_summary)

##Save the final data with new variables added
write.csv(Transportation_Estimate_Final, "/Users/reinachau/Documents/Spark Project/transportation.csv", na="", row.names=FALSE)

#Get a summary table for all parcel lands
all_land_value_transportation <- Transportation_Estimate_Final %>% 
  group_by(muni) %>% 
  summarise(total_parcel=n(), total_land_value=sum(total_value, na.rm=T)) %>% 
  replace_na(list(total_parcel=0, total_land_value=0))

#Get a summary table for all parcel lands that are non-vacant
non_vacant_value_transportation <- Transportation_Estimate_Final %>% 
  filter(!luc_adj_1 %in% 975 | !luc_adj_2  %in% 975) %>% 
  group_by(muni) %>% 
  summarise(total_non_vacant_parcel=n(), total_non_vacant_value=sum(total_value, na.rm=T)) %>% 
  replace_na(list(total_non_vacant_parcel=0, total_non_vacant_value=0))

#Get a summary table for all parcel lands that are vacant
vacant_land_value_transportation <- Transportation_Estimate_Final %>% 
  filter(luc_adj_1 %in% 975 | luc_adj_2  %in% 975) %>% 
  group_by(muni) %>% 
  summarise(total_vacant_parcel=n(), total_vacant_land_value=sum(total_value, na.rm=T)) %>% 
  replace_na(list(total_vacant_parcel=0, total_vacant_land_value=0))

#Get combined summary table
transportation_summary <- all_land_value_transportation %>% 
  left_join(vacant_land_value_transportation) %>% 
  left_join(non_vacant_value_transportation) %>% 
  replace_na(list(total_parcel=0, total_land_value=0, total_vacant_parcel=0, total_vacant_land_value=0, total_non_vacant_parcel=0, total_non_vacant_value=0)) %>% 
  arrange(desc(total_vacant_land_value), desc(total_vacant_parcel))

#Save the combined summary table
write.csv(transportation_summary, "/Users/reinachau/Documents/Spark Project/transportation_assessed_value_summary.csv", na="", row.names=FALSE)

