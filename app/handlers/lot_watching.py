from aiogram import types, Dispatcher

from utilits import compile_lot_message
from work_with_api import get_lots


async def send_lots(call: types.CallbackQuery):
    await call.message.answer('adasdasdasdasdasdd')
    # for lot in get_lots(f'@{call.from_user.username}')['lots']:
    # await call.message.answer_media_group(work_with_api.get_photos_of_lot(lot['id']),)
    # media = types.MediaGroup()
    # for image in work_with_api.get_photos_of_lot(lot['id']):

    # await bot.send_photo(call.message.chat.id, work_with_api.get_photos_of_lot(lot['id']),
    #                      caption=compile_lot_message(lot))


async def send_user_lots(call: types.CallbackQuery):
    result = get_lots(f'@{call.from_user.username}', user_lots=True)['lots']
    if len(result) != 0:
        for lot in result:
            await call.message.answer(compile_lot_message(lot))
    else:
        await call.message.answer('Объявлений нет')


def register_handlers_lot_watching(dp: Dispatcher):
    dp.register_callback_query_handler(send_user_lots, lambda call: call.data == 'user_lots', state="*")
    dp.register_callback_query_handler(send_lots, lambda call: call.data == 'view_lots', state="*")
