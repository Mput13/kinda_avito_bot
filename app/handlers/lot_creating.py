from io import BytesIO

import httpx as httpx
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import keyboards
import work_with_api


class CreateLot(StatesGroup):
    waiting_for_lot_title = State()
    waiting_for_lot_price = State()
    waiting_for_lot_description = State()
    waiting_for_lot_category = State()
    waiting_for_lot_images = State()


async def lot_creating_start(message: types.Message, state: FSMContext):
    await message.bot.send_message(message.from_user.id, "Напишите название товара")
    await state.set_state(CreateLot.waiting_for_lot_title.state)


async def title_chosen(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)

    await state.set_state(CreateLot.waiting_for_lot_price.state)
    await message.answer("Теперь отправьте цену товара")


async def lot_price_chosen(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("ТОЛЬКО ЦИФРЫ ЭТО ЖЕ ЦЕНА, СЛОМАТЬ БОТА ЗАХОТЕЛ ДА? А Я НЕ ПАЛЬЦЕМ ДЕЛАНЫЙ ИДИ ОТДЫХАЙ")
        return
    await state.update_data(price=int(message.text))
    await state.set_state(CreateLot.waiting_for_lot_description.state)
    await message.answer("Отправьте описание свое товара")


async def lot_description_chosen(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CreateLot.waiting_for_lot_category.state)
    await message.answer("Какая категория у вашего товара?")


async def lot_category_chosen(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    lot_data = await state.get_data()
    lot_data['creator'] = f'@{message.from_user.username}'
    res = await work_with_api.create_lot(lot_data)
    await state.update_data(id=res.get('id'))
    await state.set_state(CreateLot.waiting_for_lot_images.state)
    await message.answer("Отправьте фото своего товара ОДНИМ сообщением")


async def lot_images_chosen(message: types.Message, state: FSMContext):
    async with httpx.AsyncClient() as client:
        files_ids = []
        file = await message.photo[-1].get_file()
        buffer = BytesIO()
        await file.download(destination_file=buffer)
        buffer.seek(0)
        response = await client.post('http://127.0.0.1:8005//upload-image',
                                     files={'file': buffer})
        file_id = response.json()['id']
        files_ids.append(file_id)

        lot_data = await state.get_data()
        response = await client.post('http://127.0.0.1:8005//api/v2/images',
                                     json={'file_ids': files_ids, 'lot_id': lot_data['id']})
        if response.json().get('success'):
            await message.answer('Лот создан', reply_markup=keyboards.start_keyboard())
            await state.finish()
        else:
            await message.answer('Что-то пошло не так, с этим как то сам разбирайся',
                                 reply_markup=keyboards.start_keyboard())


def register_handlers_lot_creating(dp: Dispatcher):
    dp.register_callback_query_handler(lot_creating_start, lambda call: call.data == 'create_lot', state="*")
    dp.register_message_handler(title_chosen, state=CreateLot.waiting_for_lot_title)
    dp.register_message_handler(lot_price_chosen, state=CreateLot.waiting_for_lot_price)
    dp.register_message_handler(lot_description_chosen, state=CreateLot.waiting_for_lot_description)
    dp.register_message_handler(lot_category_chosen, state=CreateLot.waiting_for_lot_category)
    dp.register_message_handler(lot_images_chosen, state=CreateLot.waiting_for_lot_images,
                                content_types=types.ContentType.PHOTO)
