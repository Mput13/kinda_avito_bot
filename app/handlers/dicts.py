import json
import pprint
import time

from work_with_api import get_coordinates

articles = {"Тут будет ваша статья 1": "aboba", "Тут будет ваша статья 2": "aboba",
            "Тут будет ваша статья 3": "aboba",
            "Тут будет ваша статья 4": "aboba"}
with open('C:/Users/mputi/PycharmProjects/kinda_avito_bot/1 (2).json') as f:
    data = json.load(f)
var = data
cities = var.keys()
# for city in cities:
#     for el in var[city]:
#         lat, long = get_coordinates(el["adress"])
#         el["lat"] = lat
#         el["long"] = long
#         time.sleep(1.0)
# new_dct = {}
# for el in var:
#     city = el["adress"].split(", ")[0].strip().replace("г.", "")
#     new_dct[city] = []
#     for el1 in var:
#         if city in el1["adress"]:
#             new_dct[city].append(el1)
#             var.remove(el1)
# pprint.pprint(new_dct)
