import requests
import csv
import time
import json
import pandas as pd
import sys


"""
This script will allow you to enter the EIN's as strings into the list called
charities so it is added to a file called go.txt found in the same folder
as this file.

Things to look out for:
- the EIN's must be strings
- the Subscription key is a trial key and there are rougly 130 calls left
- there must already be a file called go.txt (or whatever you choose in
    the same folder as this file)
- The API will only allow for about 5 calls for every 30 seconds

E - Name
F - EIN
CT-CU - Total revenue:
CV - Contributions:
CW - Gov't grants:
CX - Program services:
CY - Investments:
CZ - Special events:
DA - Sales:
DB - Other:
DY - Total expenses:
DE - Program services:
DD - Administration:
DF - Fundraising:
"""

charities = ["enter charity EIN's here or read from CSV"]

def charToJson():

    counter = 1

    for x in charities:
        organization_id = x

        response = requests.get(f"https://apidata.guidestar.org/premier/v3/{organization_id}",
         headers={
           "Subscription-Key": "secret"
         }
        )

        with open("go2.txt", "a") as myfile:
            myfile.write(response.text)

        counter += 1

        if (counter%5 == 0):
            time.sleep(30)

    
"""
Inputting a JSON file to https://json-csv.com/ will manually parse through the CSV
- Currently testing ways to complete this step with pandas
"""


    
            
        
