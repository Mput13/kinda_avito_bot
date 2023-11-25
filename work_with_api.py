import pprint

import httpx
import requests

from utilits import transliterate


def get_city_from_coordinates(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    response = requests.get(url)
    data = response.json()
    pprint.pprint(data)
    return data["address"].get("city")


def get_coordinates(address):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'format': 'json',
        'q': "Russia, " + transliterate(address)
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    else:
        return None

