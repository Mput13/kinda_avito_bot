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


async def category_chosen(message: types.Message, state: FSMContext):
    result = await get_lots(f'@{message.from_user.username}', category=message.text)
    await message.answer(f'Объявления по категории {message.text}', reply_markup=types.ReplyKeyboardRemove())
    if len(result['lots']) != 0:
        for lot in result['lots']:
            await bot.send_media_group(message.chat.id,
                                       media=create_media_group(await get_photos_of_lot(lot['id'])))
            await message.answer(compile_lot_message(lot), reply_markup=start_keyboard())
    else:
        await message.answer('Объявлений нет', reply_markup=start_keyboard())
    await state.finish()


def register_handlers_watch_by_category(dp: Dispatcher):
    dp.register_callback_query_handler(category_peaking_start, lambda call: call.data == 'watch_by_categories',
                                       state="*")
    dp.register_message_handler(category_chosen, state=WatchByCategory.waiting_for_category)
