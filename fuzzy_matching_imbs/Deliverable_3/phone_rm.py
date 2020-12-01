import pandas as pd
import phonenumbers

def import_data_nat(filename):
	df = pd.read_excel(filename,names=['name','address','city','state','zipcode','phone','location','latitude','longitude','googlePlaceID'],dtype={'name': str, 'address': str, 'city':str, 'state':str, 'zipcode':str,'phone': str, 'location':dict, 'latitude': float, 'longitude': float,'googlePlaceID': str})
	df = df[df.state=='AL']

	return df

def import_data_rm(filename):
	
	df = pd.read_excel(filename, usecols="A:H", names=['imb_id', 'name', 'phone', 'address1', 'address2', 'latitude', 'longitude', 'location_hash'], dtype={'imb_id': str, 'name': str, 'phone': str, 'address1': str, 'address2': str, 'latitude': float, 'longitude': float,'location_hash': str})
	# for i in range(len(df['address'])):
	# 	addr_list = df['address'][i].split(', ')
		# if addr_list[-2]!='MA':
		# 	df.drop([i],inplace=True)
	#print(df)
	return df

def standardize_E164(df):
	for i,row in df.iterrows():
		if not isinstance(df['phone'][i], str):
			df.replace({'phone': i}, None)
			continue
		if df['phone'][i] == '0':
			df.replace({'phone':i}, None)
			continue
		pn = df['phone'][i].split(',')
		for j in range(len(pn)):
			x = phonenumbers.parse(pn[j], 'US')
			pn[j] = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.E164)
		seperator = ','
		n = seperator.join(pn)
		df.replace({df['phone'][i]:n}, inplace=True)
	return df

def E164_rm(df):
	for i, row in df.iterrows():
		#ns = df['phone'][i].strip('[]')
		ns = df['phone'][i].replace('[','')
		ns = ns.replace(']','')
		ns = ns.replace('"','')
		#print(ns)
		if row['phone']=='':
			df.replace({'phone': i}, None)
			continue
		if not isinstance(df['phone'][i], str):
			df.replace({'phone': i}, None)
			continue
		ns = ns.split(',')
		print(ns)
		for n in range(len(ns)):
			#ns[n] = ns[n].strip('[""]')
			if ns[n] == '':
				continue
			x = phonenumbers.parse(ns[n], 'US')
			ns[n] = phonenumbers.format_number(x,phonenumbers.PhoneNumberFormat.E164)
		seperator = ','
		n = seperator.join(ns)
		print(n)
		df.replace({df['phone'][i]:n}, inplace=True)
	return df




if __name__ == '__main__':
	#nat_data = import_data_nat('data/Nat-Massage-Parlors2.xlsx')
	rm_data = import_data_rm('data/RM-Full.xlsx')
	#print(E164_rm(rm_data))
	E164_rm(rm_data)
	
	#standardize_E164(nat_data)
	# print(nat_data['phone'])
	#nat_data.to_excel('data/nat_AL.xlsx')
	rm_data.to_excel('data/rm_all.xlsx')
	
