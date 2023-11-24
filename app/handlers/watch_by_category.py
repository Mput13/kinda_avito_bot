import pprint

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards import start_keyboard
from main import bot
from utilits import compile_lot_message, create_media_group
from work_with_api import get_categories, get_lots, get_photos_of_lot


class WatchByCategory(StatesGroup):
    waiting_for_category = State()


async def category_peaking_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup()
    categories = await get_categories()
    for category in categories['categories']:
        if category:
            button = types.KeyboardButton(text=category)
            keyboard.add(button)
    await message.bot.send_message(message.from_user.id, "Выберите категорию", reply_markup=keyboard)
    await state.set_state(WatchByCategory.waiting_for_category.state)


async def category_chosen(message: types.Message):
    lat = message.location.latitude
    long = message.location.longitude
    geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Yowser/2.5 Safari/537.36")
    location = geolocator.reverse(str(lat), str(long))


def register_handlers_watch_by_category(dp: Dispatcher):
    dp.register_callback_query_handler(category_peaking_start, lambda call: call.data == 'watch_by_categories',
                                       state="*")
    dp.register_message_handler(category_chosen, state=WatchByCategory.waiting_for_category)
