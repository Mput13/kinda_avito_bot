from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State

from app.handlers.dicts import var
from work_with_api import get_city_from_coordinates


class CreateLot(StatesGroup):
    coords = State()


async def lot_watching(message: types.Message):
    lat = message.location.latitude
    long = message.location.longitude
    city = get_city_from_coordinates(lat, long)
    for el in var[city]:
        text = f"""{el['type']}
{el['address']}
Можно сдать: {', '.join(el['list'])}"""
        await message.answer(text)


def register_handlers_lot_watching(dp: Dispatcher):
    dp.register_callback_query_handler(lot_watching, lambda call: call.data == 'view_lots', state="*")
