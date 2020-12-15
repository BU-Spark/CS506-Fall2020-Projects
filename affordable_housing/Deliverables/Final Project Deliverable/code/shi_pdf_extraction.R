

#R package to extract pdf
library(pdftools)
library(tidyverse)
library(stringi)

#Read in the pdf file
pdf_file <- "/Users/reinachau/Documents/Spark Project/SHI 4-24-19 (internal use).pdf"
pdf <- pdf_text(pdf_file)  %>% strsplit(split = "\n")

#Create a data frame to store the housing information for each town
Page_1=NULL
Order=NULL
Town_City_1=NULL
DHCD_ID=NULL
Project_Name=NULL
Address=NULL
Type=NULL
Total_SHI_Units=NULL
Affordability_Expires=NULL
Built_with_Comp_Permit=NULL
Subsidizing_Agency=NULL

#Create a data frame to store the percent subsidized for each town
Page_2=NULL
Town_City_2=NULL
Town_SHI_Total=NULL
Census_2010_Housing_Units=NULL
Percent_Subsidized=NULL

#Extract only the Percent Subsidized from each town
for(p in 1:length(pdf)){
  #p=18;
  print(p)
  text = pdf[[p]]
  
  #Getting the town name
  split_town <- unlist(strsplit(as.character(text[2]), "Built w/")) %>% trimws()
  town_name = split_town[1]
  
  #extract the rest rest of the 
  start_pos <- grep("Agency", text)[1] + 1
  #print(start_pos)
  
  #check if the page has the percent subsidized
  end_pos <- grep(town_name, text) %>% tail(., 1) - 1
  #print(end_pos)
  
  #Create a list entry
  Entry = NULL
  
  for(t in start_pos[1]:end_pos[1]){
    #t=11;
    
    #check if the page contains the town Totals
    str_pos_1 <- grep(paste0(town_name, " Totals"), text[t])
    
    #check if the page has percent subsidized
    str_pos_2 <- grep("Percent Subsidized", text[t])
    
    #if not, then just extract the housing information
    if(length(str_pos_1) == 0 & length(str_pos_2) == 0){
      
      split_str <- read.fwf(textConnection(as.character(text[t])), widths=c(16, 39, 43, 19, 18, 20, 14, 20)) %>% unlist() %>% trimws()
      
      if(length(split_str) == 8 & length(which(!split_str %in% c(NA, ""))) > 4){
        Page_1 <- c(Page_1, p)
        Entry <- c(Entry, ifelse(is.null(Entry), 1, Entry[length(Entry)] + 1))
        Town_City_1 <- c(Town_City_1, town_name)
        DHCD_ID <- c(DHCD_ID, split_str[1])
        Project_Name <- c(Project_Name, split_str[2]) 
        Address <- c(Address, split_str[3])
        Type <- c(Type, split_str[4])
        Total_SHI_Units <- c(Total_SHI_Units, split_str[5])
        Affordability_Expires <- c(Affordability_Expires, split_str[6])
        Built_with_Comp_Permit <- c(Built_with_Comp_Permit, split_str[7])
        Subsidizing_Agency <- c(Subsidizing_Agency, split_str[8])
      }else{
        DHCD_ID[length(DHCD_ID)] <- ifelse(!is.na(split_str[1]) & substr(split_str[1],1,1) == toupper(substr(split_str[1],1,1)), paste0(DHCD_ID[length(DHCD_ID)], ", ", split_str[1]), ifelse(!is.na(split_str[1]) & substr(split_str[1],1,1) == tolower(substr(split_str[1],1,1)), paste0(DHCD_ID[length(DHCD_ID)], split_str[1]), DHCD_ID[length(DHCD_ID)]))
        Project_Name[length(Project_Name)] <- ifelse(!is.na(split_str[2]) & substr(split_str[2],1,1) == toupper(substr(split_str[2],1,1)), paste0(Project_Name[length(Project_Name)], ", ", split_str[2]), ifelse(!is.na(split_str[2]) & substr(split_str[2],1,1) == tolower(substr(split_str[2],1,1)), paste0(Project_Name[length(Project_Name)], split_str[2]), Project_Name[length(Project_Name)])) 
        Address[length(Address)] <- ifelse(!is.na(split_str[3]) & substr(split_str[3],1,1) == toupper(substr(split_str[3],1,1)), paste0(Address[length(Address)], " ", split_str[3]), ifelse(!is.na(split_str[3]) & substr(split_str[3],1,1) == tolower(substr(split_str[3],1,1)), paste0(Address[length(Address)], split_str[3]), Address[length(Address)])) 
        Type[length(Type)] <- ifelse(!is.na(split_str[4]) & substr(split_str[4],1,1) == toupper(substr(split_str[4],1,1)), paste0(Type[length(Type)], ", ", split_str[4]), ifelse(!is.na(split_str[4]) & substr(split_str[4],1,1) == tolower(substr(split_str[4],1,1)), paste0(Type[length(Type)], split_str[4]), Type[length(Type)])) 
        Total_SHI_Units[length(Total_SHI_Units)] <- ifelse(!is.na(split_str[5]) & substr(split_str[5],1,1) == toupper(substr(split_str[5],1,1)), paste0(Total_SHI_Units[length(Total_SHI_Units)], ", ", split_str[5]), ifelse(!is.na(split_str[5]) & substr(split_str[5],1,1) == tolower(substr(split_str[5],1,1)), paste0(Total_SHI_Units[length(Total_SHI_Units)], split_str[5]), Total_SHI_Units[length(Total_SHI_Units)])) 
        Affordability_Expires[length(Affordability_Expires)] <- ifelse(!is.na(split_str[6]) & substr(split_str[6],1,1) == toupper(substr(split_str[6],1,1)), paste0(Affordability_Expires[length(Affordability_Expires)], ", ", split_str[6]), ifelse(!is.na(split_str[6]) & substr(split_str[6],1,1) == tolower(substr(split_str[6],1,1)), paste0(Affordability_Expires[length(Affordability_Expires)], split_str[6]), Affordability_Expires[length(Affordability_Expires)])) 
        Built_with_Comp_Permit[length(Built_with_Comp_Permit)] <- ifelse(!is.na(split_str[7]) & substr(split_str[7],1,1) == toupper(substr(split_str[7],1,1)), paste0(Built_with_Comp_Permit[length(Built_with_Comp_Permit)], ", ", split_str[7]), ifelse(!is.na(split_str[7]) & substr(split_str[7],1,1) == tolower(substr(split_str[7],1,1)), paste0(Built_with_Comp_Permit[length(Built_with_Comp_Permit)], split_str[7]), Built_with_Comp_Permit[length(Built_with_Comp_Permit)])) 
        Subsidizing_Agency[length(Subsidizing_Agency)] <- ifelse(!is.na(split_str[8]) & substr(split_str[8],1,1) == toupper(substr(split_str[8],1,1)), paste0(Subsidizing_Agency[length(Subsidizing_Agency)], ", ", split_str[8]), ifelse(!is.na(split_str[8]) & substr(split_str[8],1,1) == tolower(substr(split_str[8],1,1)), paste0(Subsidizing_Agency[length(Subsidizing_Agency)], split_str[8]), Subsidizing_Agency[length(Subsidizing_Agency)])) 
      }
      
    }else{
      
      #if yes, then extract SHI total
      if(length(str_pos_1) > 0){
        #Getting the page and town name
        Page_2 <- c(Page_2, p)
        Town_City_2 <- c(Town_City_2, town_name)
        
        #Getting the SHI total
        split_total <- unlist(strsplit(as.character(text[t]), paste0(town_name, " Totals"))) %>% trimws() %>% stri_remove_empty() %>% strsplit(., paste0("Census 2010 Year Round Housing Units")) %>% unlist() %>% trimws() %>% stri_remove_empty() 
        Town_SHI_Total = c(Town_SHI_Total, split_total[1])
        Census_2010_Housing_Units = c(Census_2010_Housing_Units, split_total[2])
      }
      
      #if yes, then extract the percent subsidized
      if(length(str_pos_2) > 0){
        #Getting the percent subsidized
        split_percent <- unlist(strsplit(as.character(text[t]), "Percent Subsidized")) %>% trimws() %>% stri_remove_empty() 
        Percent_Subsidized = c(Percent_Subsidized, split_percent[1])
      }
      
    }
  }
  
  Order <- c(Order, Entry)
  
}

#Clean up the data frame where some pages does not contain the percent of subsidized
final_housing_inventory = data.frame(
  Page_1=Page_1,
  Order=Order,
  Town_City_1=Town_City_1,
  DHCD_ID=DHCD_ID,
  Project_Name=Project_Name,
  Address=Address,
  Type=Type,
  Total_SHI_Units=Total_SHI_Units,
  Affordability_Expires=Affordability_Expires,
  Built_with_Comp_Permit=Built_with_Comp_Permit,
  Subsidizing_Agency=Subsidizing_Agency,
  stringsAsFactors=FALSE
) %>% rename(Page=Page_1, Town_or_City=Town_City_1)

#Create a data frame to store the percent subsidized for each town
final_percent_subsidized = data.frame(
  Page_2=Page_2,
  Town_City_2=Town_City_2,
  Town_SHI_Total=Town_SHI_Total,
  Census_2010_Housing_Units=Census_2010_Housing_Units,
  Percent_Subsidized=Percent_Subsidized,
  stringsAsFactors=FALSE
) %>% rename(Page=Page_2, Town_or_City=Town_City_2)

#Save the final copy to a csv file
write_csv(final_housing_inventory, "/Users/reinachau/Documents/Spark Project/final_housing_inventory.csv")
write_csv(final_percent_subsidized, "/Users/reinachau/Documents/Spark Project/final_percent_subsidized.csv")


