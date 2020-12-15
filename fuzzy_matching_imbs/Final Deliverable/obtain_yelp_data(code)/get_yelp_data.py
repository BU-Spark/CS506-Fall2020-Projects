from __future__ import print_function

import argparse
import configparser
import json
import pprint
import requests
import sys
import urllib


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
config = configparser.ConfigParser()
config.read('keys')
API_KEY= config['DEFAULT']['API_key']


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'massage'
DEFAULT_LOCATION = '13210'
SEARCH_LIMIT = 50
DEFAULT_OFFSET = 0
SEARCH_CATEGORY = 'Massage'
API_COUNT = 0

def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location, offset):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'offset': offset,
        'categories': SEARCH_CATEGORY

    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location, offset):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location, offset)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return []

    # business_id = businesses[0]['id']

    # print(u'{0} businesses found, querying business info ' \
    #     'for the top result "{1}" ...'.format(
    #         len(businesses), business_id))
    # response = get_business(API_KEY, business_id)

    # print(u'Result for business "{0}" found:'.format(business_id))
    # pprint.pprint(response, indent=2)
    return businesses

def offset_run(term, location, offset, businesses):
    if offset>950: 
        with open('data/data_'+location+'.json','w') as f:
            json.dump(businesses, f)
        return businesses

    scrolled = query_api(term, location, offset)
    global API_COUNT
    API_COUNT = API_COUNT + 1
    if scrolled:
        businesses += scrolled
        print('loaded...{0}'.format(len(businesses)))
        if len(scrolled)==50:
            offset_run(term, location, offset+50, businesses)
        else:
            with open('data/data_'+location+'.json','w') as f:
                json.dump(businesses, f)
    else:
        with open('data/data_'+location+'.json','w') as f:
            json.dump(businesses, f)

    return businesses


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')
    parser.add_argument('-o', '--offset', dest='offset',
                        default=DEFAULT_OFFSET, type=int,
                        help='Search offset (default: %(default)s)')

    input_values = parser.parse_args()

    try:

        businesses = offset_run(input_values.term, input_values.location, input_values.offset, [])
        print(API_COUNT)
        #print(len(businesses))
        #query_api(input_values.term, input_values.location, input_values.offset)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()