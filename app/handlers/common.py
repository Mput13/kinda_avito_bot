from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards import start_keyboard
from work_with_api import create_user


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    username = message.from_user.username
    create_user(f'@{username}')
    await message.answer('че надо', reply_markup=start_keyboard())


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Что-нибудь ещё?', reply_markup=start_keyboard())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
