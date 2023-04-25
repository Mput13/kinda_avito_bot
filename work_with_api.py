from base64 import b64decode as dec64
from io import BytesIO

import requests
from PIL import Image


def create_user(username):
    result = requests.post('http://127.0.0.1:8005/api/v2/users', json={'telegram_id': username})
    return result


def get_lots(username, user_lots=False):
    if user_lots:
        return requests.get(f'http://127.0.0.1:8005//api/v2/lots?watcher={username}&user_lots=True').json()
    else:
        return requests.get(f'http://127.0.0.1:8005//api/v2/lots?watcher={username}').json()


def get_all_lots():
    return requests.get(f'http://127.0.0.1:8005//api/v2/lots').json()


def get_categories():
    return requests.get(f'http://127.0.0.1:8005//api/v2/categories').json()


def create_lot(dct):
    return requests.post('http://127.0.0.1:8005//api/v2/lots',
                         json=dct).json()


def add_images(path, lot_id, files):
    return requests.post('http://127.0.0.1:8005//api/v2/images', files=files, json={'path': path,
                                                                                    'lot_id': lot_id}).json()


def get_photos_of_lot(lot_id):
    result = requests.get(f'http://127.0.0.1:8005//api/v2/images/{lot_id}').json()
    output = []
    for binary_image in result['photos']:
        image = Image.open(BytesIO(dec64(binary_image)))
        output.append(image)
    return output
