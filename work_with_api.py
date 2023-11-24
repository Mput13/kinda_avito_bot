import pprint

import httpx
import requests


def get_city_from_coordinates(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    response = requests.get(url)
    data = response.json()
    return data["address"].get("city")

print(get_city_from_coordinates("61.0093556", "69.0308561"))

async def create_user(username):
    async with httpx.AsyncClient() as client:
        return await client.post('http://127.0.0.1:8005/api/v2/users', json={'telegram_id': username})
    # return map([post('http://127.0.0.1:8005/api/v2/users', json={'telegram_id': username})])[0].json()


async def get_lots(username, user_lots=False, category=None):
    async with httpx.AsyncClient() as client:
        if category:
            res = await client.get(f'http://127.0.0.1:8005//api/v2/lots', params={'category': category})
            return res.json()
        elif user_lots:
            res = await client.get(f'http://127.0.0.1:8005//api/v2/lots', params={'watcher': username,
                                                                                  'user_lots': True})
            return res.json()
        else:
            res = await client.get(f'http://127.0.0.1:8005//api/v2/lots', params={'watcher': username})
            return res.json()


async def get_all_lots():
    async with httpx.AsyncClient() as client:
        res = await client.get(f'http://127.0.0.1:8005//api/v2/lots')
        return res.json()


async def get_categories():
    async with httpx.AsyncClient() as client:
        res = await client.get(f'http://127.0.0.1:8005//api/v2/categories')
        return res.json()


async def create_lot(dct):
    async with httpx.AsyncClient() as client:
        res = await client.post('http://127.0.0.1:8005//api/v2/lots',
                                json=dct)
        return res.json()


async def delete_lot(id, user):
    async with httpx.AsyncClient() as client:
        res = await client.delete(f'http://127.0.0.1:8005//api/v2/lots/{id}', params={'user': user})
    return res.json()


async def get_photos_of_lot(lot_id):
    async with httpx.AsyncClient() as client:
        result = await client.get(f'http://127.0.0.1:8005//api/v2/images/{lot_id}')
        output = []
        for id in result.json()['image_ids']:
            res = await client.get(f'http://127.0.0.1:8005//get-image', params={'image_id': id})
            output.append(res.content)
    return output
