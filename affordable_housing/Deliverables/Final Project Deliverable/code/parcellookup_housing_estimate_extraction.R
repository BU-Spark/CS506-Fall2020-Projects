
###scraped the html page 
library(rvest)
library(xml2)
library(RCurl)
library(XML)
library(httr)
library(jsonlite)
library(tidyverse)

#Read in the Housing dataset
Housing <- read.csv("/Users/reinachau/Documents/Spark Project/housing.csv", stringsAsFactors=FALSE)

#Create a data frame to store the values
Housing_Estimate <- data.frame(
  index=Housing$index,
  mapc_id=Housing$mapc_id,
  parloc_id=Housing$parloc_id,
  search_addr_num=Housing$addr_num,
  search_addr_str=Housing$addr_str,
  search_owner_city=Housing$owner_city,
  search_owner_state="MA",
  search_owner_zip=Housing$owner_zip,
  match_parcel_id=NA,
  result_url=NA,
  parcel_address=NA,
  parcel_id=NA,
  total_assessed_value=NA,
  tax_year_1=NA,
  land_area=NA,
  land_use=NA,
  assessed_land_value=NA,
  tax_year_2=NA,
  year_built=NA,
  assessed_building_value=NA,
  tax_year_3=NA,
  last_sale_price=NA,
  last_sale_date=NA,
  owner=NA,
  owner_address=NA,
  parcel_on_this_street_1=NA,
  parcel_value_1=NA,
  parcel_owner_1=NA,
  parcel_on_this_street_2=NA,
  parcel_value_2=NA,
  parcel_owner_2=NA,
  parcel_on_this_street_3=NA,
  parcel_value_3=NA,
  parcel_owner_3=NA,
  parcel_on_this_street_4=NA,
  parcel_value_4=NA,
  parcel_owner_4=NA,
  parcel_on_this_street_5=NA,
  parcel_value_5=NA,
  parcel_owner_5=NA,
  parcel_on_this_street_6=NA,  
  parcel_value_6=NA,
  parcel_owner_6=NA,
  parcel_on_this_street_7=NA,
  parcel_value_7=NA,
  parcel_owner_7=NA,
  parcel_on_this_street_8=NA,
  parcel_owner_8=NA,
  parcel_value_8=NA,
  parcel_on_this_street_9=NA,
  parcel_value_9=NA,
  parcel_owner_9=NA,
  parcel_on_this_street_10=NA,
  parcel_value_10=NA,
  parcel_owner_10=NA,
  avg_parcel_value_on_this_street=NA,
  parcel_with_similar_value_in_this_area_1=NA,  
  similar_parcel_value_1=NA,
  similar_parcel_owner_1=NA,
  parcel_with_similar_value_in_this_area_2=NA,
  similar_parcel_value_2=NA,
  similar_parcel_owner_2=NA,
  parcel_with_similar_value_in_this_area_3=NA,
  similar_parcel_value_3=NA,
  similar_parcel_owner_3=NA,
  parcel_with_similar_value_in_this_area_4=NA,
  similar_parcel_value_4=NA,
  similar_parcel_owner_4=NA,
  parcel_with_similar_value_in_this_area_5=NA,
  similar_parcel_value_5=NA,
  similar_parcel_owner_5=NA,
  parcel_with_similar_value_in_this_area_6=NA,
  similar_parcel_value_6=NA,
  similar_parcel_owner_6=NA,
  parcel_with_similar_value_in_this_area_7=NA,
  similar_parcel_value_7=NA,
  similar_parcel_owner_7=NA,
  parcel_with_similar_value_in_this_area_8=NA,
  similar_parcel_value_8=NA,
  similar_parcel_owner_8=NA,
  parcel_with_similar_value_in_this_area_9=NA,
  similar_parcel_value_9=NA,
  similar_parcel_owner_9=NA,
  parcel_with_similar_value_in_this_area_10=NA,
  similar_parcel_value_10=NA,
  similar_parcel_owner_10=NA,
  avg_similar_parcel_value_in_this_area=NA
)

#filter parcels that has completed addresses and zipcode
listpos <- which(Housing_Estimate$match_parcel_id %in% c(NA) & !Housing_Estimate$search_addr_num %in% c(NA, "", " ") & !Housing_Estimate$search_addr_str %in% c(NA, "", " ") & !Housing_Estimate$search_owner_city %in% c(NA, "", " ") & !Housing_Estimate$search_owner_zip %in% c(NA, "", " "))

for(k in listpos){
  #k=1
  addr_num = gsub(" ", "+", Housing_Estimate$search_addr_num[k])
  addr_str = gsub(" ", "+", Housing_Estimate$search_addr_str[k])
  addr_city = gsub(" ", "+", Housing_Estimate$search_owner_city[k]) %>% gsub(",", "", .)
  addr_state = gsub(" ", "+", Housing_Estimate$search_owner_state[k])
  addr_zip = gsub(" ", "+", Housing_Estimate$search_owner_zip[k]) %>% strsplit(., "-") %>% unlist() %>% first()
  
  if(nchar(addr_zip) < 5){
    addr_zip <- paste0(paste0(rep(0, 5-nchar(addr_zip)), collapse=""), addr_zip,  collapse="")
  }else if(nchar(addr_zip) > 5){
    addr_zip <- substr(addr_zip, 1, 5)
  }
  
  parcel_full_address = paste0(addr_num, "+", addr_str, "%2C+", addr_city, "%2C+", addr_state, "+", addr_zip)
  parcellookup <- read_html(paste0("https://parcellookup.com/search?q=", parcel_full_address))
  
  ##Extract the url link
  posExtractStart <- gregexpr("<a href=\"/p/", parcellookup, fixed = TRUE)[[1]]
  
  if(posExtractStart[1] < 0){
    
    Housing_Estimate$match_parcel_id[k] <- "No Match"
    
    next
    
  }else if(posExtractStart[1] > 0){
    
    # extract string of 200 characters length
    stringExtract <- substring(parcellookup, first=posExtractStart, last = posExtractStart + 100) %>% unique(.)
    
    #Extract the Zillow URL that has the information about the property
    URL = unlist(lapply(1:length(stringExtract), function(l){ 
      #l=1;
      address = parcel_full_address %>% gsub("[+]", "-", .) %>% gsub("%2C", "", .) %>% tolower()
      
      #posStart <- gregexpr(address, stringExtract[l], fixed = TRUE)[[1]][1]
      posStart <- agrep(address, stringExtract[l], max=8)
      
      if(length(posStart) == 0){
        return(NULL)
      }else{
        # extract string of 200 characters length
        string <- substring(stringExtract[l] %>% gsub("<a href=\"/p/", "", .), first=posStart, last = posStart + 100)[[1]][1]
        split <- strsplit(as.character(string), "\"", fixed=TRUE)[[1]][1]
        return(split)
      }
    })) %>% unique()
    
    if(length(URL) == 0){
      
      Housing_Estimate$match_parcel_id[k] <- "No Match"
      
      next
      
    }else if(length(URL) > 0){
      
      for(u in 1:length(URL)){
        #u=1;
        #get the url text
        resultURL <- paste0("https://parcellookup.com/p/", URL[u])
        siteHTML <- read_html(resultURL)
        
        tbls <- siteHTML %>%
          html_nodes("table")
        
        tbls_ls <- tbls %>%
          .[1:length(tbls)] %>%
          html_table(fill = TRUE)
        
        if(length(tbls_ls) == 0){
          
          Housing_Estimate$match_parcel_id[k] <- "No Match"
          
          next 
          
        }else if(length(tbls_ls) > 0){
          
          ##Get the list values###
          list_data_1 <- tbls_ls[[1]]
          
          search_parcel_id <- list_data_1$X2[which(list_data_1$X1 %in% "Parcel ID")]
          parcel_id <- Housing_Estimate$parloc_id[k]
          
          if(search_parcel_id != parcel_id){
            
            Housing_Estimate$match_parcel_id[k] <- "No Match"
            
            next
            
          }else if(search_parcel_id == parcel_id){
            
            ##print the parcel entry
            print(Housing_Estimate$index[k])
            
            ##store the match value
            Housing_Estimate$match_parcel_id[k] <- TRUE
            
            #Store the result url
            Housing_Estimate$result_url[k] <- resultURL[1]
            
            ###########################################################################################################################################################
            
            Housing_Estimate$parcel_address[k] <- list_data_1$X2[which(list_data_1$X1 %in% "Parcel Address")]
            Housing_Estimate$parcel_id[k] <- list_data_1$X2[which(list_data_1$X1 %in% "Parcel ID")]
            Housing_Estimate$total_assessed_value[k] <- list_data_1$X2[which(list_data_1$X1 %in% "Total Assessed Value")] %>% gsub("[$]", "", .) %>% gsub("[,]","", .) %>% as.numeric()
            Housing_Estimate$tax_year_1[k] <- list_data_1$X2[which(list_data_1$X1 %in% "Tax Year")]
            
            ###########################################################################################################################################################
            
            if(length(tbls_ls) > 1){
              
              list_data_2 <- tbls_ls[[2]]
              
              Housing_Estimate$land_area[k] <- list_data_2$X2[which(list_data_2$X1 %in% "Land Area")]
              Housing_Estimate$land_use[k] <- list_data_2$X2[which(list_data_2$X1 %in% "Land Use")]
              Housing_Estimate$assessed_land_value[k] <- list_data_2$X2[which(list_data_2$X1 %in% "Assessed Land Value")] %>% gsub("[$]", "", .) %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$tax_year_2[k] <- list_data_2$X2[which(list_data_2$X1 %in% "Tax Year")]
              
            }      
            ###########################################################################################################################################################
            
            if(length(tbls_ls) > 2){
              
              list_data_3 <- tbls_ls[[3]]
              
              Housing_Estimate$year_built <- list_data_3$X2[which(list_data_3$X1 %in% "Year Built")]
              Housing_Estimate$assessed_building_value[k] <- list_data_3$X2[which(list_data_3$X1 %in% "Assessed Building Value")] %>% gsub("[$]", "", .) %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$tax_year_3[k] <- list_data_3$X2[which(list_data_3$X1 %in% "Tax Year")]
              
            }
            
            ###########################################################################################################################################################
            
            if(length(tbls_ls) > 3){
              
              list_data_4 <- tbls_ls[[4]]
              
              Housing_Estimate$last_sale_price[k] <- list_data_4$X2[which(list_data_4$X1 %in% "Last Sale Price")] %>% gsub("[$]", "", .) %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$last_sale_date[k] <- list_data_4$X2[which(list_data_4$X1 %in% "Last Sale Date")]
              
            }
            
            ###########################################################################################################################################################
            
            if(length(tbls_ls) > 4){
              
              list_data_5 <- tbls_ls[[5]]
              
              Housing_Estimate$owner[k] <- list_data_5$X2[which(list_data_5$X1 %in% "Owner")]
              Housing_Estimate$owner_address[k] <- list_data_5$X2[which(list_data_5$X1 %in% "Owner Address")]
              
            }
            
            ###########################################################################################################################################################
            
            if(length(tbls_ls) > 5){
              
              list_data_6 <- tbls_ls[[6]]
              
              Housing_Estimate$parcel_on_this_street_1[k] <- list_data_6$X1[1] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_on_this_street_2[k] <- list_data_6$X1[2] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_on_this_street_3[k] <- list_data_6$X1[3] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_on_this_street_4[k] <- list_data_6$X1[4] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_on_this_street_5[k] <- list_data_6$X1[5] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_on_this_street_6[k] <- list_data_6$X1[6] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_on_this_street_7[k] <- list_data_6$X1[7] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_on_this_street_8[k] <- list_data_6$X1[8] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_on_this_street_9[k] <- list_data_6$X1[9] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_on_this_street_10[k] <- list_data_6$X1[10] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              
              Housing_Estimate$parcel_owner_1[k] <- list_data_6$X1[1] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$parcel_owner_2[k] <- list_data_6$X1[2] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$parcel_owner_3[k] <- list_data_6$X1[3] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$parcel_owner_4[k] <- list_data_6$X1[4] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$parcel_owner_5[k] <- list_data_6$X1[5] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$parcel_owner_6[k] <- list_data_6$X1[6] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$parcel_owner_7[k] <- list_data_6$X1[7] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$parcel_owner_8[k] <- list_data_6$X1[8] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$parcel_owner_9[k] <- list_data_6$X1[9] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$parcel_owner_10[k] <- list_data_6$X1[10] %>% strsplit(., "\n") %>% unlist() %>% last()
              
              Housing_Estimate$parcel_value_1[k] <- list_data_6$X1[1] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$parcel_value_2[k] <- list_data_6$X1[2] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$parcel_value_3[k] <- list_data_6$X1[3] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$parcel_value_4[k] <- list_data_6$X1[4] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$parcel_value_5[k] <- list_data_6$X1[5] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$parcel_value_6[k] <- list_data_6$X1[6] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$parcel_value_7[k] <- list_data_6$X1[7] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$parcel_value_8[k] <- list_data_6$X1[8] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$parcel_value_9[k] <- list_data_6$X1[9] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$parcel_value_10[k] <- list_data_6$X1[10] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              
              Housing_Estimate$avg_parcel_value_on_this_street[k] <- mean(c(Housing_Estimate$parcel_value_1[k], Housing_Estimate$parcel_value_2[k], Housing_Estimate$parcel_value_3[k], Housing_Estimate$parcel_value_4[k], Housing_Estimate$parcel_value_5[k], Housing_Estimate$parcel_value_6[k], Housing_Estimate$parcel_value_7[k], Housing_Estimate$parcel_value_8[k], Housing_Estimate$parcel_value_9[k], Housing_Estimate$parcel_value_10[k]), na.rm=TRUE) 
              
            }
            
            ###########################################################################################################################################################
            
            if(length(tbls_ls) > 6){
              
              list_data_7 <- tbls_ls[[7]]
              
              Housing_Estimate$parcel_with_similar_value_in_this_area_1[k] <- list_data_7$X1[1] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_with_similar_value_in_this_area_2[k] <- list_data_7$X1[2] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_with_similar_value_in_this_area_3[k] <- list_data_7$X1[3] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_with_similar_value_in_this_area_4[k] <- list_data_7$X1[4] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_with_similar_value_in_this_area_5[k] <- list_data_7$X1[5] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_with_similar_value_in_this_area_6[k] <- list_data_7$X1[6] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_with_similar_value_in_this_area_7[k] <- list_data_7$X1[7] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_with_similar_value_in_this_area_8[k] <- list_data_7$X1[8] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_with_similar_value_in_this_area_9[k] <- list_data_7$X1[9] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              Housing_Estimate$parcel_with_similar_value_in_this_area_10[k] <- list_data_7$X1[10] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% first()
              
              Housing_Estimate$similar_parcel_owner_1[k] <- list_data_7$X1[1] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$similar_parcel_owner_2[k] <- list_data_7$X1[2] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$similar_parcel_owner_3[k] <- list_data_7$X1[3] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$similar_parcel_owner_4[k] <- list_data_7$X1[4] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$similar_parcel_owner_5[k] <- list_data_7$X1[5] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$similar_parcel_owner_6[k] <- list_data_7$X1[6] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$similar_parcel_owner_7[k] <- list_data_7$X1[7] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$similar_parcel_owner_8[k] <- list_data_7$X1[8] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$similar_parcel_owner_9[k] <- list_data_7$X1[9] %>% strsplit(., "\n") %>% unlist() %>% last()
              Housing_Estimate$similar_parcel_owner_10[k] <- list_data_7$X1[10] %>% strsplit(., "\n") %>% unlist() %>% last()
              
              Housing_Estimate$similar_parcel_value_1[k] <- list_data_7$X1[1] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$similar_parcel_value_2[k] <- list_data_7$X1[2] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$similar_parcel_value_3[k] <- list_data_7$X1[3] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$similar_parcel_value_4[k] <- list_data_7$X1[4] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$similar_parcel_value_5[k] <- list_data_7$X1[5] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$similar_parcel_value_6[k] <- list_data_7$X1[6] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$similar_parcel_value_7[k] <- list_data_7$X1[7] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$similar_parcel_value_8[k] <- list_data_7$X1[8] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$similar_parcel_value_9[k] <- list_data_7$X1[9] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              Housing_Estimate$similar_parcel_value_10[k] <- list_data_7$X1[10] %>% strsplit(., "\n") %>% unlist() %>% first() %>% gsub("[(]", "", .) %>% gsub("[)]", "", .) %>% strsplit(., "[$]") %>% unlist() %>% last() %>% gsub("[,]","", .) %>% as.numeric()
              
              Housing_Estimate$avg_similar_parcel_value_in_this_area[k] <- mean(c(Housing_Estimate$similar_parcel_value_1[k], Housing_Estimate$similar_parcel_value_2[k], Housing_Estimate$similar_parcel_value_3[k], Housing_Estimate$similar_parcel_value_4[k], Housing_Estimate$similar_parcel_value_5[k], Housing_Estimate$similar_parcel_value_6[k], Housing_Estimate$similar_parcel_value_7[k], Housing_Estimate$similar_parcel_value_8[k], Housing_Estimate$similar_parcel_value_9[k], Housing_Estimate$similar_parcel_value_10[k]), na.rm=TRUE) 
              
            }
            
            break
            
          }
        }
      }
    }
  }
}

write.csv(Housing_Estimate, "/Users/reinachau/Documents/Spark Project/Housing_Estimate.csv", na="", row.names=FALSE)

