# Run

the run.py is what you have to run to turn all the parcel coordinates into classfied images of Parking lots or None Parking lots.

## File descriptions

### screenshotScript.py & index.html

read the coordinates and obtains the images with Google StreetView API. 

### pklotClassifier.py

classify the parcel images

### v1.csv

contains the latitude and longitude of each parcel data entry

## Set up 

1. Create an empty 'predict' folder, which contains an empty 'img' folder in this directory. 

2. 'pip install tensorflow' and make sure Tensor flow version 2.3.1 and also 'pip install selenium' 

3. Download Chrome Driver and put it in this directory. download link: https://sites.google.com/a/chromium.org/chromedriver/home

4. run 'run.py'. This file will go through 'v1.csv', retrieve all the images and classifiy them into corresponding new folders. Just make sure you name the csv file as 'v1.csv' and have the same format as this current one or you can go into screenshotScript.py to modify your file path.
