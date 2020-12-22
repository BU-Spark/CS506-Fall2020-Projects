from uszipcode import SearchEngine
import sys
import pprint

def get_zipcode(state):
	zipcodes = []
	search = SearchEngine()
	res = search.by_state(state,returns=None)

	for i in range(len(res)):
		zipcodes.append(res[i].zipcode)

	return zipcodes

def split2segments(zipcodes):
	portions = len(zipcodes)//25
	segments = []
	for i in range(portions):
		segments.append(zipcodes[i*25:i*25+25])
	if len(zipcodes)%25:
		segments.append(zipcodes[portions*25:])
	return segments


def main():
	try:
		zipcodes = get_zipcode(sys.argv[1])
		print(len(zipcodes))
	except IndexError:
		sys.exit('Need to provide a state')

	f = open('data/zipcodes_'+sys.argv[1]+'.txt','w')
	pprint.pprint(split2segments(zipcodes), f)
    


if __name__ == '__main__':
	main()