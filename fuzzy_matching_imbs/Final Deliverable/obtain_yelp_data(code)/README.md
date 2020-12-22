# Obtain Yelp Data

## Approach
- Obtain data in JSON format
- Convert to CSV file
- Delete duplicate data in CSV (This step can be done in Excel)

## Instructions
- Create a file named ***keys*** under current directory
- Add your api key from yelp in the following format  
        ```
        [DEFAULT]  
        API_key = Your key here  
        ```
- Run command line followed by a state name as input:  
        ```
        python main.py  
        ```
- Change directory name ***data*** to ***state-abbr_data***
- Create a new directory named ***data*** to start over a new search


## Note:
- While Running code, make sure pay close attention to your api using limit [here](https://www.yelp.com/developers/v3/manage_app)
- For each run, the result is stored as ***./data/data.csv***
- There are a lot of extra information in final version of csv
- All json files are included in your data directory
- There is a ***data/data.json*** file under data directory might give you a warning of file too large. It's okay to ignore that.

## What does each file do
***get_zipcde.py***: retrieve all zipcodes in a given state
***search_by_zipcde.py***: using retrieved zipcode perform search
***get_yelp_data.py***: calling yelp api for searching with given zipcode, output as json files
***join_json.py***: join all json file produced into 1 (within one state)
***convert2csv.py***: select useful information from json and convert it to csv files
