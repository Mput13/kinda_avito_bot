from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards import start_keyboard
from main import bot
from utilits import compile_lot_message, create_media_group
from work_with_api import get_categories, get_lots, get_photos_of_lot, delete_lot


class UserLots(StatesGroup):
    waiting_for_id = State()


async def user_lots_delete_start(call: types.CallbackQuery, state: FSMContext):
    result = await get_lots(f'@{call.from_user.username}', user_lots=True)
    if len(result['lots']) != 0:
        for lot in result['lots']:
            await bot.send_media_group(call.from_user.id,
                                       media=create_media_group(await get_photos_of_lot(lot['id'])))
            await call.message.answer(compile_lot_message(lot))
            await call.message.answer('Если хотите удалить объявление, отправьте его номер', reply_markup=start_keyboard())
            await state.set_state(UserLots.waiting_for_id.state)
    else:
        await call.message.answer('Объявлений нет', reply_markup=start_keyboard())


async def id_chosen(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        res = await delete_lot(int(message.text), f'@{message.from_user.username}')
        if res.get('success'):
            await message.answer(f'Лот №{message.text} удален', reply_markup=start_keyboard())
        else:
            await message.answer('Вы не создатель объявления', reply_markup=start_keyboard())
        await state.finish()
    else:
        await message.answer('ЦИФРАМИ')
    await state.finish()


def register_handlers_lot_deleting(dp: Dispatcher):
    dp.register_callback_query_handler(user_lots_delete_start, lambda call: call.data == 'user_lots',
                                       state="*")
    dp.register_message_handler(id_chosen, state=UserLots.waiting_for_id)
