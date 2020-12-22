

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

Transportation <- read.csv("/Users/reinachau/Documents/Spark Project/transportation.csv", stringsAsFactors=FALSE)

#Create a dataframe to store the Zmarket values
Transportation_WalkScore_TransitScore <- data.frame(
  index = Transportation$index,
  mapc_id = Transportation$mapc_id,
  owner_city = Transportation$owner_city,
  owner_state = Transportation$owner_stat,
  latitude = Transportation$latitude,
  longitude = Transportation$longitude,
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


listpos_1 <- which(Transportation_WalkScore_TransitScore$walkscore %in% c(NA, "") & !Transportation_WalkScore_TransitScore$latitude %in% c(NA, "") & !Transportation_WalkScore_TransitScore$longitude %in% c(NA, "", " "))

for(k in listpos_1){
  #k=900;
  print(k)
  latitude = Transportation_WalkScore_TransitScore$latitude[k]
  longitude = Transportation_WalkScore_TransitScore$longitude[k]

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
  
  Transportation_WalkScore_TransitScore$walkscore_status[k] <- test_request_1
  
  if(test_request_1 == "pass"){
    request_1 <- fromJSON(rawToChar(walkscore_res$content))

    if(length(request_1[["walkscore"]]) > 0){
      Transportation_WalkScore_TransitScore$walkscore[k] <- request_1[["walkscore"]]
    }
  }
  
}

##################################################################################################################################################
#
#
# CALL TRANSIT SCORE API
#
##################################################################################################################################################

listpos_2 <- which(Transportation_WalkScore_TransitScore$transitscore %in% c(NA, "") & !Transportation_WalkScore_TransitScore$owner_city %in% c(NA, "") & !Transportation_WalkScore_TransitScore$owner_state %in% c(NA, "") & !Transportation_WalkScore_TransitScore$latitude %in% c(NA, "") & !Transportation_WalkScore_TransitScore$longitude %in% c(NA, "", " "))

for(k in listpos_2){
  #k=1;
  latitute = Transportation_WalkScore_TransitScore$latitude[k]
  longitude = Transportation_WalkScore_TransitScore$longitude[k]
  city = gsub(" ", "%20", Transportation_WalkScore_TransitScore$owner_city[k]) %>% gsub(",", "", .)
  state = gsub(" ", "%20", Transportation_WalkScore_TransitScore$owner_state[k])
  
  transitscore_URL <- paste0("https://transit.walkscore.com/transit/score/?lat=", latitute, "&lon=", longitude, "&city=", city, "&state=", state, "&wsapikey=", API_Key)
  
  transitscore_res <- GET(url=transitscore_URL, accept_json())
  
  #extract the url from Zillow
  test_request_2 <- tryCatch({
    
    stop_for_status(transitscore_res)
    
    "pass"
    
  }, error = function(e) {
    
    "fail"
    
  })
  
  Transportation_WalkScore_TransitScore$transitscore_status[k] <- test_request_2
  
  if(test_request_2 == "pass"){
    print(k)
    request_2 <- fromJSON(rawToChar(transitscore_res$content))
    Transportation_WalkScore_TransitScore$transitscore[k] <- request_2[["transit_score"]]
    Transportation_WalkScore_TransitScore$transit_score_description[k] <- request_2[["description"]]
    Transportation_WalkScore_TransitScore$transit_score_summary[k] <- request_2[["summary"]]
  }  
  
}

write.csv(Transportation_WalkScore_TransitScore, "/Users/reinachau/Documents/Spark Project/Transportation_WalkScore_TransitScore_1.csv", row.names=FALSE)

