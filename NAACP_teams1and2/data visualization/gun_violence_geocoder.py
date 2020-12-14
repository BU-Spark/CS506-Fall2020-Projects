import pandas as pd
# import geopandas as gpd
import geopy
from geopy.extra.rate_limiter import RateLimiter

# Read in the CSV file of gun violence incidents 
gv_df = pd.read_csv("gun_violence_incidents_2014-2018.csv")

# Create an instance of the geocoder and specify the delay between geocoding requests with the RateLimiter
geolocator = geopy.Nominatim(user_agent="myGeocoder")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds = 1)

# Concatenate a few columns to create a single column with the full address of each incident
gv_df['Full Address'] = gv_df['Address'] + "," + gv_df['City Or County'] + "," + gv_df['State']

# Use the geocoder functionality to obtain the location (verbose address) and the point (latitude, longitude, and altitude) of each entry
gv_df['Location'] = gv_df['Full Address'].apply(geocode)
gv_df['Point'] = gv_df['Location'].apply(lambda loc: tuple(loc.point) if loc else None)

# Filter out the entries for which the geocoder output "None", as they will be of no use
not_none = gv_df['Point'] == gv_df['Point']
gv_df_filtered = gv_df[not_none]

# Split the tuple to create individual columns for each field 
gv_df_filtered[['Latitude', 'Longitude', 'Altitude']] = pd.DataFrame(gv_df_filtered['Point'].tolist(), index=gv_df_filtered.index)
print(gv_df_filtered)

# Convert our updated DataFrame to a new CSV file 
gv_df_filtered.to_csv("gv_incidents_geocoded.csv", index=False)
