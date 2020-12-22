# Parking Lot Project CS506
## Deliverable 1 10/28

- Hanyu Chen
- Israel Ramirez
- Hsin-Hung Wu


About the data we have collected until right now, we tried to use Google API to get the image of vacant parcels. The first thing we did is to get the data that labeled as vacant land. We select it by using tax exempt codes. After that, we pre-processing the data, which store them as a list of locations.

The next step we have done is to obtain the images of locations, by using corresponding longitude and latitude. We tried to write a script of HTML, and use the Google API to collect them. The code is uploaded as GoogleAPI.html. However, here comes a problem. Since Google dose not allow us to store the images from Google Map, this method may violate some rules.

Due to this reason, we tried to use another database called MassGIS's Online Mapping Tool. It contains different kinds of maps and different years of map, which is more helpful to analyze the change of parking lots.

Another problem is about the raw data. In some database, we can get the location represented by longitude and latitude, but no all of the databases have this attribute. We may need to ask Mario in the next meeting.

