import pandas as pd
import numpy as np

def import_data_nat(filename):
	df = pd.read_excel(filename,names=['label','name','address','city','state','zipcode','phone','location','latitude','longitude','googlePlaceID'],dtype={'label':str, 'name': str, 'address': str, 'city':str, 'state':str, 'zipcode':str,'phone': str, 'location':dict, 'latitude': float, 'longitude': float,'googlePlaceID': str})
	df.drop(columns=['label', 'location'], inplace=True)
	return df


def import_data_rm(filename):
	df = pd.read_excel(filename,names=['label','imb_idx','name','phone','address','address2','latitude','longitude','location_hash'],dtype={'label':str,'imb_idx':str,'name': str, 'phone': str, 'address': str, 'address2': str, 'latitude': float, 'longitude': float,'location_hash': str})
	df.drop(columns=['label','address2'],inplace=True)
	return df

def addr_split_nat(df):
	rest = []
	for i in df['address']:
		if not i: 
			rest.append('')
		else:
			ad = i.split(', ')
			ad.pop(-1)
			rest.append(' '.join(x for x in ad))
	df['addr'] = rest
	df.drop(columns=['address'],inplace=True)
	df.sort_values(by=['zipcode'],inplace=True)
	
	return df

def addr_split_rm(df):
	state = []
	zipcode = []
	rest = []
	for i in df['address']:
		if not i:
			state.append('')
			zipcode.append('')
			rest.append('')
		else:
			ad = i.split(', ')

			state.append(ad[-2])
			zipcode.append(ad[-1].replace(' ','')[:5])
			ad.pop(-1)
			ad.pop(-1)
			rest.append(' '.join(x for x in ad))
	df['state'] = state
	df['zipcode'] = zipcode
	df['addr'] = rest

	df.drop(columns=['address'], inplace=True)
	df.sort_values(by=['zipcode'],inplace=True)
	
	return df



if __name__ == '__main__':
	# st = ['AK','AL','AR','AZ','CA','CO','CT','DC','DE','FL']
	# st = ["GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA"]
	# st = ["ME", "MD", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR"]
	#st = ["PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
	st = ['MA']
	for s in st:
		nat_data = import_data_nat('raw/nat_'+s+'.xlsx')
		addr_split_nat(nat_data)
		nat_data.to_excel('clean/nat_'+s+'.xlsx')

	# rm_data = import_data_rm('raw/rm_all.xlsx')
	# addr_split_rm(rm_data)
	# rm_data.to_excel('clean/rm_all.xlsx')
	# 