import json
import pandas as pd
import csv

def json2csv(json_file):
	df = pd.read_json(json_file)
	print(len(df))
	df.drop_duplicates(subset=['id'], inplace=True, ignore_index=True)
	print(len(df))
	#addresses = []
	address1 = [] 
	address2 = []
	address3 = []
	city = []
	zip_code = []
	country = []
	state = []
	#display_address = []
	
	longitudes = []
	latitudes = []

	for i in range(len(df)):
		try:
			address1.append(df['location'][i]['address1'])
		except KeyError:
			address1.append('')

		try:
			address2.append(df['location'][i]['address2'])
		except KeyError:
			address2.append('')

		try:
			address3.append(df['location'][i]['address3'])
		except KeyError:
			address3.append('')

		try:
			city.append(df['location'][i]['city'])
		except KeyError:
			city.append('')

		try:
			zip_code.append(df['location'][i]['zip_code'])
		except KeyError:
			zip_code.append('')

		try:
			country.append(df['location'][i]['country'])
		except KeyError:
			country.append('')

		try:
			state.append(df['location'][i]['state'])
		except KeyError:
			state.append('')


		try:
			longitudes.append(df['coordinates'][i]['longitude'])	
		except KeyError:
			longitudes.append(None)

			
		try:
			latitudes.append(df['coordinates'][i]['latitude'])
		except KeyError:
			latitudes.append(None)
			
	df['address1'] = address1
	df['address2'] = address2
	df['address3'] = address3
	df['city'] = city
	df['zip_code'] = zip_code
	df['country'] = country
	df['state'] = state
	df['longitude'] = longitudes
	df['latitude'] = latitudes
	df.drop(columns=['alias','image_url','is_closed','url','review_count','categories','rating','coordinates','transactions','price','location','display_phone','distance'],inplace=True)

	df.to_csv('MA_data/data.csv',index=False)



if __name__ == '__main__':
	json2csv('MA_data/MA.json')