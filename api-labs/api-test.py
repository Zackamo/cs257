#!/usr/bin/env python3
'''
    api-test.py
    Zack Johnson, 25 October 2021

    Adapted from an example by: Jeff Ondich, Updated 7 October 2020

    An example for CS 257 Software Design. How to retrieve results
    from an HTTP-based API, parse the results (JSON in this case),
    and manage the potential errors.
'''

import sys
import json
import urllib.request

API_BASE_URL = 'http://api.covidtracking.com'

def print_state_deaths(state):
    url = f'{API_BASE_URL}/vi/states/{state}/daily.json'
    data_from_server = urllib.request.urlopen(url).read()
    string_from_server = data_from_server.decode('utf-8')
    covid_days = json.loads(string_from_server)
    result_list = []
    print("Date    Deaths")
    for day in covid_days:
        print(f"{day["date"]}:", day["deaths"])

def main(args):
    get_state_deaths('mn')

if __name__ == '__main__':
    main()
