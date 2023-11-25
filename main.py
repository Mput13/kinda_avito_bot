import logging

from aiogram import Bot, executor
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import work_with_api
from utilits import compile_lot_message
from work_with_api import get_lots, get_categories

# Объект бота
bot = Bot(token="6086685442:AAEmMuHTw8ceN8dczxvaN8HujPbsHBE25Rk", parse_mode="HTML")
# Диспетчер для бота
dp = Dispatcher(bot, storage=MemoryStorage())
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


class CreateLot(StatesGroup):
    waiting_for_names = State()


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('Отправьте через пробел все имена')
    await state.set_state()


@dp.callback_query_handler(text="view_lots")
async def send_lots(call: types.CallbackQuery, state: FSMContext):
    for lot in get_lots(f'@{call.from_user.username}')['lots']:
        await bot.send_photo(call.message.chat.id, work_with_api.get_photos_of_lot(lot['id']),
                             caption=compile_lot_message(lot))


@dp.callback_query_handler(text="user_lots")
async def send_user_lots(call: types.CallbackQuery):
    result = get_lots(f'@{call.from_user.username}', user_lots=True)['lots']
    if len(result) != 0:
        for lot in result:
            await call.message.answer(compile_lot_message(lot))
    else:
        await call.message.answer('Объявлений нет')


@dp.callback_query_handler(text="get_category_buttons")
async def get_all_categories(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup()
    for category in get_categories()['categories']:
        button = types.KeyboardButton(text=category)
        keyboard.add(button)
    await call.message.answer('Выберите категорию', reply_markup=keyboard)


#     нужно добавить состояние ожидания любого сообщения на которое он ответит лотами или как то по другому

@dp.callback_query_handler(text="create_lot")
async def create_lot(call: types.CallbackQuery):
    pass


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
    register_handlers_lot_creating(dp)
