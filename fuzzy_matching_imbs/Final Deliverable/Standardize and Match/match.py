import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

def load_yelp(state):
	df_yelp = pd.read_excel('clean/yelp_'+state+'.xlsx',usecols=[1,2,3,4,5,6,7,8,9],dtype={'id':str, 'name': str, 'city':str, 'state':str, 'zip_code':str, 'phone': str, 'longitude': float, 'latitude': float, 'addr': str})
	return df_yelp

def load_nat(state):
	"""load data from google places"""
	df_nat = pd.read_excel('clean/nat_'+state+'.xlsx',usecols=[1,2,3,4,5,6,7,8,9],
		names=['name','city','state','zipcode','phone','latitude','longitude','googlePlaceID','addr'],
		dtype={'name': str, 'address': str, 'city':str, 'state':str, 'zipcode':str,'phone': str, 'location':dict, 'latitude': float, 'longitude': float,'googlePlaceID': str})
	return df_nat

def load_rm():
	"""load data from rubmaps"""
	df_rm = pd.read_excel('clean/rm_all.xlsx',usecols=[1,2,3,4,5,6,7,8,9],
		names=['imb_idx','name','phone','latitude','longitude','location_hash','state','zipcode','addr'],
		dtype={'imb_idx':str,'name': str, 'phone': str, 'latitude': float, 'longitude': float,'location_hash': str,'state': str,'zipcode':str ,'addr':str})
	return df_rm

def match_gp(df_nat, df_rm, state):
	# prepare lists for matching by zipcode
	googleID = []
	location_hash = []
	name_addr_score = []
	addr_score = []
	name_score = []
	phone_score = []
	city = []

	google_ad = []
	rubmap_ad = []
	g_phone = []
	r_phone = []

	# iterate over rows in gp and rm and match the same zipcodes. row_t is a row from google places, and row is row from rubmaps
	for i, row in df_rm.iterrows():
		temp = df_nat[df_nat.zipcode==row.zipcode]
		for j, row_t in temp.iterrows():
			a = row['name']+', '+row['addr']
			b = row_t['name']+', '+row_t['addr']
			googleID.append(row_t['googlePlaceID'])
			location_hash.append(row['location_hash'])
			addr_score.append(fuzz.token_set_ratio(row['addr'],row_t['addr']))
			phone_score.append(fuzz.token_set_ratio(row['phone'],row_t['phone']))
			name_addr_score.append(fuzz.token_set_ratio(a,b))
			name_score.append(fuzz.token_set_ratio(row['name'],row_t['name']))
			google_ad.append(b)
			rubmap_ad.append(a)
			g_phone.append(row_t['phone'])
			r_phone.append(row['phone'])
			city.append(row_t['city'])
        
	# append each column into a new df
	df_score = pd.DataFrame()
	df_score['location_hash'] = location_hash
	df_score['googleID'] = googleID
	df_score['rubmap_ad'] = rubmap_ad
	df_score['google_ad'] = google_ad
	df_score['name_score'] = name_score
	df_score['addr_score'] = addr_score
	df_score['name_addr_score'] = name_addr_score
	df_score['g_phone'] = g_phone
	df_score['r_phone'] = r_phone
	df_score['phone_score'] = phone_score
	df_score['city'] = city
	print(df_score)

	# filtering df_score to eliminate rows with combined score lower than 90
	df_score = df_score[df_score['name_addr_score']>=90]

	# assign tiers to each row based on matching score
	tier = []
	for i, row in df_score.iterrows():
		if df_score['name_addr_score'][i]==100 and df_score['phone_score'][i]==100:
			tier.append(1)
		elif df_score['name_addr_score'][i]==100 and df_score['phone_score'][i]!=100:
			tier.append(2)
		elif df_score['addr_score'][i]==100 or df_score['name_score'][i]==100 and df_score['phone_score'][i]==100:
			tier.append(3)
		elif df_score['addr_score'][i]==100 and df_score['name_score'][i]!=100 and df_score['phone_score']!=100:
			tier.append(4)
		else:
			tier.append(5)
	df_score['tier'] = tier
	df_score.to_excel('data/high_chance_'+state+'.xlsx')

def match_yelp(df_yelp, df_rm,state):
	# prepare lists for matching stores
	yelp_id = []
	location_hash = []
	name_addr_score = []
	addr_score = []
	name_score = []
	phone_score = []
	city = []

	yelp_ad = []
	rubmap_ad = []
	g_phone = []
	r_phone = []
	# iterate through rubmap and yelp data
	for i, row in df_rm.iterrows():
		temp = df_yelp[df_yelp['zip_code']==row['zipcode']]
		for j, row_t in temp.iterrows():
			a = row['name']+', '+row['addr']
			b = row_t['name']+', '+row_t['addr']
			yelp_id.append(row_t['id'])
			location_hash.append(row['location_hash'])
			addr_score.append(fuzz.token_set_ratio(row['addr'],row_t['addr']))
			phone_score.append(fuzz.token_set_ratio(row['phone'],row_t['phone']))
			name_addr_score.append(fuzz.token_set_ratio(a,b))
			name_score.append(fuzz.token_set_ratio(row['name'],row_t['name']))
			yelp_ad.append(b)
			rubmap_ad.append(a)
			g_phone.append(row_t['phone'])
			r_phone.append(row['phone'])
			city.append(row_t['city'])
	# store matching results in another df
	df_score = pd.DataFrame()
	df_score['location_hash'] = location_hash
	df_score['yelp_id'] = yelp_id
	df_score['rubmap_ad'] = rubmap_ad
	df_score['yelp_ad'] = yelp_ad
	df_score['name_score'] = name_score
	df_score['addr_score'] = addr_score
	df_score['name_addr_score'] = name_addr_score
	df_score['g_phone'] = g_phone
	df_score['r_phone'] = r_phone
	df_score['phone_score'] = phone_score
	df_score['city'] = city

	print(df_score)
	# filtering df_score
	df_score = df_score[df_score['name_addr_score']>=90]
	tier = []
	# assign tier with matching score
	for i, row in df_score.iterrows():
		if df_score['name_addr_score'][i]==100 and df_score['phone_score'][i]==100:
			tier.append(1)
		elif df_score['name_addr_score'][i]==100 and df_score['phone_score'][i]!=100:
			tier.append(2)
		elif df_score['addr_score'][i]==100 or df_score['name_score'][i]==100 and df_score['phone_score'][i]==100:
			tier.append(3)
		elif df_score['addr_score'][i]==100 and df_score['name_score'][i]!=100 and df_score['phone_score']!=100:
			tier.append(4)
		else:
			tier.append(5)
	df_score['tier'] = tier
	# store results in a spreadsheet
	df_score.to_excel('data/high_chance_y_'+state+'.xlsx')

if __name__ == '__main__':
	df_rm = load_rm()
	st = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "MA", "ME", "MD", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
	
	for s in st:
		df_nat = load_nat(s)
		match_gp(df_nat, df_rm, s)
	# df_yelp = load_yelp('MA')
	# match_yelp(df_yelp,df_rm, 'MA')