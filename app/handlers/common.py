from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.handlers.dicts import var
from keyboards import start_keyboard
from work_with_api import get_city_from_coordinates, get_coordinates


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    username = message.from_user.username
    await message.answer('Главное меню', reply_markup=start_keyboard())


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Что-нибудь ещё?', reply_markup=start_keyboard())


async def handle_location(message: types.Message, state: FSMContext):
    # Получаем координаты местоположения пользователя
    lat = message.location.latitude
    long = message.location.longitude
    city = get_city_from_coordinates(lat, long).replace('городской округ ', '')
    # lat, long = get_coordinates(['adress'])
    for el in var[city]:
        text = f"""{types.ContentType.LOCATION()}
{el['type']}
    {el['adress']}
    Можно сдать: {', '.join(el['list'])}"""
        await message.answer(text)
    await state.finish()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(handle_location, content_types=types.ContentType.LOCATION)
