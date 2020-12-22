import pandas as pd

def merge_gp_res():
	st = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "MA", "ME", "MD", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
	frames = []
	for s in st:
		df = pd.read_excel('data/high_chance_'+s+'.xlsx')
		df['state'] = s
		frames.append(df)
	res = pd.concat(frames)
	res.to_excel('data/gp_res.xlsx')


if __name__ == '__main__':
	merge_gp_res()