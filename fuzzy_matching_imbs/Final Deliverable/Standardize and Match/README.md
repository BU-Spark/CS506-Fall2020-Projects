# Description of Matching
- Three folders raw, clean, data should be created under the same directory as scripts. Input data, rubmap data and google places data should be stored in data folder. Scraped yelp data can go directly to raw.  

- First run standardize_phone to get standardized phone number of rubmap and google places. It also splits google places data into smaller chunks (in state) as standardization phone. It output files to folder raw.  

- To standardize addresses, run functions from addr_std.py. In this file, it takes input from raw folder and output to clean folder.  

- matching.py include all matching functions. It takes input from clean and output it to data folder. 

- Note: all initial input and final output are in data folder