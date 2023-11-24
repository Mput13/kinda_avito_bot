from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateLot(StatesGroup):
    coords = State()


async def lot_watching(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Пожалуйста, отправьте свое местоположение",
                                   reply_markup=types.ReplyKeyboardRemove())


def register_handlers_lot_watching(dp: Dispatcher):
    dp.register_callback_query_handler(lot_watching, lambda call: call.data == 'view_lots', state="*")
