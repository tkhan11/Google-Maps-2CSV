# -*- coding: utf-8 -*-
"""
File Name: GoogleMaps2CSV.py
Created On: Sat July 27th, 2024 20:44:06
Description: This file contains the main script to get the search keyword google maps information and store the extracted info to a csv file.
Author: Tanveer Khan

"""

import math
import re
import requests
import json
import pandas as pd

# Constants
EARTH_RADIUS_IN_METERS = 6371010
TILE_SIZE = 256
SCREEN_PIXEL_HEIGHT = 768
RADIUS_X_PIXEL_HEIGHT = 27.3611 * EARTH_RADIUS_IN_METERS * SCREEN_PIXEL_HEIGHT

PAGINATION_PARAMETERS_REGEX = re.compile(
    r"@\s*(?P<latitude>[-+]?\d{1,2}(?:[.,]\d+)?)\s*,\s*(?P<longitude>[-+]?\d{1,3}(?:[.,]\d+)?)\s*,\s*(?P<zoom>\d{1,2}(?:[.,]\d+)?)z", 
    re.VERBOSE
)

def altitude(zoom, latitude):
    return str((RADIUS_X_PIXEL_HEIGHT * math.cos(math.radians(latitude))) / ((2 ** zoom) * TILE_SIZE))

def pagination(location_lat_long, start_offset):
    extracted_parameters = PAGINATION_PARAMETERS_REGEX.match(location_lat_long)
    if not extracted_parameters:
        return ""
    return (
        "!4m8!1m3!1d" +
        altitude(float(extracted_parameters['zoom']), float(extracted_parameters['latitude'])) +
        "!2d" +
        extracted_parameters['longitude'] +
        "!3d" +
        extracted_parameters['latitude'] +
        "!3m2!1i1024!2i768!4f13.1!7i20!8i" +
        str(start_offset) +
        "!10b1!12m25!1m1!18b1!2m3!5m1!6e2!20e3!6m16!4b1!23b1!26i1!27i1!41i2!45b1!49b1!63m0!67b1!73m0!74i150000!75b1!89b1!105b1!109b1!110m0!10b1!16b1!19m4!2m3!1i360!2i120!4i8!20m65!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m50!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0!22m3!1s!2z!7e81!24m55!1m15!13m7!2b1!3b1!4b1!6i1!8b1!9b1!20b0!18m6!3b1!4b1!5b1!6b1!13b0!14b0!2b1!5m5!2b1!3b1!5b1!6b1!7b1!10m1!8e3!14m1!3b1!17b1!20m4!1e3!1e6!1e14!1e15!24b1!25b1!26b1!29b1!30m1!2b1!36b1!43b1!52b1!54m1!1b1!55b1!56m2!1b1!3b1!65m5!3m4!1m3!1m2!1i224!2i298!89b1!26m4!2m3!1i80!2i92!4i8!30m28!1m6!1m2!1i0!2i0!2m2!1i458!2i768!1m6!1m2!1i974!2i0!2m2!1i1024!2i768!1m6!1m2!1i0!2i0!2m2!1i1024!2i20!1m6!1m2!1i0!2i748!2m2!1i1024!2i768!34m16!2b1!3b1!4b1!6b1!8m4!1b1!3b1!4b1!6b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!37m1!1e81!42b1!46m1!1e9!47m0!49m1!3b1!50m53!1m49!2m7!1u3!4s!5e1!9s!10m2!3m1!1e1!2m7!1u2!4s!5e1!9s!10m2!2m1!1e1!2m7!1u16!4s!5e1!9s!10m2!16m1!1e1!2m7!1u16!4s!5e1!9s!10m2!16m1!1e2!3m11!1u16!2m4!1m2!16m1!1e1!2s!2m4!1m2!16m1!1e2!2s!3m1!1u2!3m1!1u3!4BIAE!2e2!3m1!3b1!59B!65m0!69i540"
    )

def fetch_places_data(location_lat_long, start_offset, search_keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': "place_your_cookie_here",
        'Referer': 'https://www.google.com/',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    params = {
        'tbm': 'map',
        'authuser': '0',
        'hl': 'en',
        'pb': pagination(location_lat_long, start_offset),
        'q': search_keyword,
        'tch': '1',
        'ech': '5',
    }

    url = "https://www.google.com/search"
    response = requests.get(url, params=params, headers=headers)
    data = json.loads(response.text[:-6])['d'][5:]
    places_data = json.loads(data)[0][1]

    places_dict = {
        "name": [place[14][11] for place in places_data[1:]],
        "address": [place[14][2][0] for place in places_data[1:]],
        "website": [place[14][7][0] if place[14][7] else 'None' for place in places_data[1:]],
        "phone_number": [place[14][178][0] if place[14][178] else 'None' for place in places_data[1:]],
        "open_close_timing": [
            {day[0]: day[1][0].replace('\u202f', ' ') for day in place[14][34][1]} if place[14][34] and place[14][34][1] else None
            for place in places_data[1:]
        ],
        "ratings": [place[14][4][7] if place[14][4] else None for place in places_data[1:]],
        "reviews": [place[14][4][3][1] if place[14][4] else None for place in places_data[1:]],
        "gmap_link": [
            'https://www.google.com/maps/place/?q=place_id:' + re.search(r"placeid=([^\&]+)", place[14][4][3][0]).group(1)
            if place[14][4] else None
            for place in places_data[1:]
        ]
    }

    return places_dict

def save_to_csv(places_dict, search_keyword):
    filename = search_keyword + ".csv"
    df = pd.DataFrame(places_dict)
    df['address'] = df['address'].astype(str).str.replace('[', '').str.replace(']', '')
    df = df[['name', 'phone_number', 'ratings', 'reviews', 'website', 'address', 'gmap_link', 'open_close_timing']]
    df.to_csv(filename, index=False)

# Example usage
location_lat_long = "@26.410369869420826,74.63477731779587,11z"
# search_keyword = 'Neurologist'
search_keyword = 'Marriage Gardens'

# Fetch data in increments of 20 for pagination
all_places = {
    "name": [],
    "address": [],
    "website": [],
    "phone_number": [],
    "open_close_timing": [],
    "ratings": [],
    "reviews": [],
    "gmap_link": []
}

for start_offset in range(0, 1000, 20):  # Change 100 to your desired max number of places
    places_dict = fetch_places_data(location_lat_long, start_offset, search_keyword)
    
    # Append the new data to the overall dictionary
    for key in all_places:
        all_places[key].extend(places_dict.get(key, []))

save_to_csv(all_places, search_keyword)
