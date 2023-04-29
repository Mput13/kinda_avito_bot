import io
import os
import tempfile
from base64 import encodebytes

from aiogram import types


def compile_lot_message(lot: dict):
    return f"""Объявление №{lot['id']} ⬆️⬆️⬆️
{lot['title']} {lot['price']}
{lot['description']}
{lot['creator']}"""


def get_bite_image(file):
    byte_arr = io.BytesIO()
    file.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
    return encoded_img


def create_media_group(lst):
    media = types.MediaGroup()
    for file in lst:
        with open('./newfile.jpg', 'wb') as target:
            target.write(file)
            media.attach_photo(types.InputFile('./newfile.jpg'))
    return media
