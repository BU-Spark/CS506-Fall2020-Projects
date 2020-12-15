

#R PACKAGES
###scraped the html page 
library(rvest)
library(xml2)
library(RCurl)
library(XML)
library(httr)
library(jsonlite)
library(tidyverse)

API_Key <- "719e7a58daf25647275ff58942226b56"

Housing <- read.csv("/Users/reinachau/Documents/Spark Project/housing.csv", stringsAsFactors=FALSE)

#Create a dataframe to store the Zmarket values
Housing_WalkScore_TransitScore <- data.frame(
  index = Housing$index,
  mapc_id = Housing$mapc_id,
  owner_city = Housing$owner_city,
  owner_state = Housing$owner_stat,
  latitude = Housing$latitude,
  longitude = Housing$longitude,
  walkscore=NA,
  walkscore_status=NA,
  transitscore=NA,
  transitscore_status=NA,
  transit_score_description=NA, 
  transit_score_summary=NA
)

##################################################################################################################################################
#
#
# CALL WALK SCORE API
#
##################################################################################################################################################


listpos_1 <- which(Housing_WalkScore_TransitScore$walkscore %in% c(NA, "") & !Housing_WalkScore_TransitScore$latitude %in% c(NA, "") & !Housing_WalkScore_TransitScore$longitude %in% c(NA, "", " "))

for(k in listpos_1){
  #k=900;
  print(k)
  latitude = Housing_WalkScore_TransitScore$latitude[k]
  longitude = Housing_WalkScore_TransitScore$longitude[k]
  
  walkscore_URL <- paste0("http://api.walkscore.com/score?format=json&lat=", latitude, "&lon=", longitude, "&wsapikey=", API_Key)
  
  walkscore_res <- GET(
    url = walkscore_URL,
    accept_json()
  )
  
  #extract the url from Zillow
  test_request_1 <- tryCatch({
    
    stop_for_status(walkscore_res)
    
    "pass"
    
  }, error = function(e) {
    
    "fail"
    
  })
  
  Housing_WalkScore_TransitScore$walkscore_status[k] <- test_request_1
  
  if(test_request_1 == "pass"){
    request_1 <- fromJSON(rawToChar(walkscore_res$content))
    
    if(length(request_1[["walkscore"]]) > 0){
      Housing_WalkScore_TransitScore$walkscore[k] <- request_1[["walkscore"]]
    }
  }
  
}

##################################################################################################################################################
#
#
# CALL TRANSIT SCORE API
#
##################################################################################################################################################


listpos_2 <- which(Housing_WalkScore_TransitScore$transitscore %in% c(NA, "") & !Housing_WalkScore_TransitScore$owner_city %in% c(NA, "") & !Housing_WalkScore_TransitScore$owner_state %in% c(NA, "") & !Housing_WalkScore_TransitScore$latitude %in% c(NA, "") & !Housing_WalkScore_TransitScore$longitude %in% c(NA, "", " "))

for(k in listpos_2){
  #k=1;
  latitute = Housing_WalkScore_TransitScore$latitude[k]
  longitude = Housing_WalkScore_TransitScore$longitude[k]
  city = gsub(" ", "%20", Housing_WalkScore_TransitScore$owner_city[k]) %>% gsub(",", "", .)
  state = gsub(" ", "%20", Housing_WalkScore_TransitScore$owner_state[k])
  
  transitscore_URL <- paste0("https://transit.walkscore.com/transit/score/?lat=", latitute, "&lon=", longitude, "&city=", city, "&state=", state, "&wsapikey=", API_Key)
  
  transitscore_res <- GET(url=transitscore_URL, accept_json())

  #extract the url from Zillow
  test_request_2 <- tryCatch({
    
    stop_for_status(transitscore_res)
    
    "pass"
    
  }, error = function(e) {
    
    "fail"
    
  })
  
  Housing_WalkScore_TransitScore$transitscore_status[k] <- test_request_2
  
  if(test_request_2 == "pass"){
    print(k)
    request_2 <- fromJSON(rawToChar(transitscore_res$content))
    Housing_WalkScore_TransitScore$transitscore[k] <- request_2[["transit_score"]]
    Housing_WalkScore_TransitScore$transit_score_description[k] <- request_2[["description"]]
    Housing_WalkScore_TransitScore$transit_score_summary[k] <- request_2[["summary"]]
  }  
  
}

write.csv(Housing_WalkScore_TransitScore, "/Users/reinachau/Documents/Spark Project/Housing_WalkScore_TransitScore_1.csv", row.names=FALSE)
