import glob
import json

def join_data(path):
	files = glob.glob(path)
	res = []
	for file in sorted(files):
		with open(file, 'r') as f:
			res += json.load(f)
	output = json.dumps(res)
	f_w = open('data/data.json', 'w')
	json.dump(res[0:], f_w)

def main():
	path = 'data/data_*.json'
	join_data(path)

if __name__ == '__main__':
	main()