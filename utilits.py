import io
import os
import tempfile
import uuid
from base64 import encodebytes

from aiogram import types
# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="Tester")
# adress = str(input('Введите адрес: \n'))
# location = geolocator.geocode(adress)
# print(location.latitude, location.longitude)

categories = '''бумага
пластик
стекло
металл
тетра-пак
одежда
лампочки
крышечки
техника
батареки
шины
опасное
другое'''.split('\n')


def transliterate(text):
    # Словарь для транслитерации
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g',
        'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
        'я': 'ya',
    }

    result = ''
    for char in text:
        if char.lower() in translit_dict:
            if char.isupper():
                result += translit_dict[char.lower()].capitalize()
            else:
                result += translit_dict[char]
        else:
            result += char
    return result


def get_bite_image(file):
    byte_arr = io.BytesIO()
    file.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
    return encoded_img


def create_media_group(lst):
    media = types.MediaGroup()
    for file in lst:
        name = f'./files/{uuid.uuid4()}.jpeg'
        with open(name, 'wb') as target:
            target.write(file)
            media.attach_photo(types.InputFile(name))
    return media
