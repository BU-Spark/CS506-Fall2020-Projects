import pandas as pd
import phonenumbers

def import_data_nat(filename):
	df_nat = pd.read_excel('data/Nat-Massage-Parlors2.xlsx',names=['name','address','city','state','zipcode','phone','location','latitude','longitude','googlePlaceID'], dtype={'name': str, 'address': str, 'city':str, 'state':str, 'zipcode':str,'phone': str, 'location':dict, 'latitude': float, 'longitude': float,'googlePlaceID': str})

	return df_nat

def import_data_rm(filename):
	df = pd.read_excel(filename, usecols="A:H", names=['imb_id', 'name', 'phone', 'address1', 'address2', 'latitude', 'longitude', 'location_hash'], dtype={'imb_id': str, 'name': str, 'phone': str, 'address1': str, 'address2': str, 'latitude': float, 'longitude': float,'location_hash': str})
	# for i in range(len(df['address'])):
	# 	addr_list = df['address'][i].split(', ')
		# if addr_list[-2]!='MA':
		# 	df.drop([i],inplace=True)
	#print(df)
	return df

def E164_rm(df):
	"""standardize rubmap phone"""
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
	df.to_excel('raw/rm_all.xlsx')
	return df

def E164_nat(df_nat):
	"""Google places phone std"""
	st = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "MA", "ME", "MD", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
	# standardize phone by state, for organization purpose
	for s in st:
		df = df_nat[df_nat.state==s]
		for i,row in df.iterrows():
			if not isinstance(df['phone'][i], str):
				df.replace({'phone': i}, None)
				continue
			if df['phone'][i] == '0':
				df.replace({'phone':i}, None)
				continue
			pn = df['phone'][i]
			print(i)
       
        try:
            x = phonenumbers.parse(pn, 'US')
            pn = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.E164)
            df.replace({df['phone'][i]:pn}, inplace=True)
        except phonenumbers.NumberParseException:
            df.replace({'phone': i}, None, inplace=True)
    	# storing into a spreadsheet, path is subject to change
    	df.to_excel('raw/nat_'+s+'.xlsx')


if __name__ == '__main__':
	nat_data = import_data_nat('data/Nat-Massage-Parlors2.xlsx')
	rm_data = import_data_rm('data/RM-Full.xlsx')
	
	E164_rm(rm_data)
	E164_nat(na_data)
	#rm_data.to_excel('data/rm_all.xlsx')
	
