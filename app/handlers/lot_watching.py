from aiogram import types, Dispatcher

from keyboards import start_keyboard
from main import bot
from utilits import compile_lot_message, create_media_group
from work_with_api import get_lots, get_photos_of_lot


async def send_lots(call: types.CallbackQuery):
    await call.message.answer('adasdasdasdasdasdd')
    result = await get_lots(f'@{call.from_user.username}')
    if len(result['lots']) != 0:
        for lot in result['lots']:
            await bot.send_media_group(call.message.chat.id,
                                       media=create_media_group(await get_photos_of_lot(lot['id'])))
            await call.message.answer(compile_lot_message(lot), reply_markup=start_keyboard())
    else:
        await call.message.answer('Объявлений нет', reply_markup=start_keyboard())


def register_handlers_lot_watching(dp: Dispatcher):
    dp.register_callback_query_handler(send_lots, lambda call: call.data == 'view_lots', state="*")
