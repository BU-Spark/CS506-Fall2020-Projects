from get_zipcode import get_zipcode, split2segments
from join_json import join_data
from search_by_zipcode import run_api
from convert2csv import json2csv

import sys

def main():
	try:
		zipcodes = split2segments(get_zipcode(sys.argv[1]))
	except IndexError:
		sys.exit('Need to provide a state')

	for segment in zipcodes:
		run_api(segment)

	path = 'data/data_*.json'
	join_data(path)

	json2csv('data/data.json')

if __name__ == '__main__':
	main()