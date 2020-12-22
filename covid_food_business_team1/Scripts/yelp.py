import requests
import json


def get_businesses(location, term, api_key, number_of_query, offset):
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'

    data = []
    for counter in range(0, number_of_query, 50):
        params = {
            'limit': 50,
            'location': location.replace(' ', '+'),
            'term': term.replace(' ', '+'),
            'offset': counter + offset
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data += response.json()['businesses']
        elif response.status_code == 400:
            print('400 Bad Request')
            break

    return data


def main():
    api_key = "INSERT API KEY HERE"

    location = "boston"
    term = "restaurant"
    """
    after searching online, it turns out yelp api only supports returning less than 1000 records
    nothing i can do with that
    """
    NUM_RECORDS = 1000
    for i in range(int(NUM_RECORDS / 1000)):
        res = get_businesses(location, term, api_key, 1000, i * 1000)
        print("current number of records", len(res))
        with open('data.json', 'a+') as outfile:
            json.dump(res, outfile)

main()
