from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = 'YOUR_API_KEY'

google_places = GooglePlaces(YOUR_API_KEY)

# You may prefer to use the text_search API, instead.
query_result = google_places.text_search(query = 'Restaurant in Boston',location='Boston, United States',radius=20000)
# If types param contains only 1 item the request to Google Places API
# will be send as type param to fullfil:
# http://googlegeodevelopers.blogspot.com.au/2016/02/changes-and-quality-improvements-in_16.html

#if query_result.has_attributions:
    #print(query_result.html_attributions)

print("~~~~~~~~~~~")

i =0
num = 5

for place in query_result.places:
    # Returned places from a query are place summaries.
    print(place.name)
    print(place.geo_location)
    print(place.place_id)

    # The following method has to make a further API call.
    place.get_details()
    # Referencing any of the attributes below, prior to making a call to
    # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    print(place.details) # A dict matching the JSON response from Google.
    print(place.website)
    print(place.url)
    
    if(i == num):
      break
    i = i + 1
