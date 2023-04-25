from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

import work_with_api
from keyboards import start_keyboard


class CreateLot(StatesGroup):
    waiting_for_lot_title = State()
    waiting_for_lot_price = State()
    waiting_for_lot_description = State()
    waiting_for_lot_category = State()
    waiting_for_lot_images = State()


async def lot_creating_start(message: types.Message, state: FSMContext):
    await message.answer("Напишите название товара")
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
    id = work_with_api.create_lot(lot_data).get('id')
    await state.update_data(id=id)
    await state.set_state(CreateLot.waiting_for_lot_images.state)
    await message.answer("Отправьте фото своего товара ОДНИМ ФОТО")


async def lot_images_chosen(message: types.Message, state: FSMContext):
    photos = message.photo
    lot_data = await state.get_data()
    work_with_api.add_images(f'./lot_images/{message.from_user.username}/{lot_data["id"]}', lot_data['id'],
                             {'files': photos})
    await state.finish()
    await message.answer('Что-нибудь ещё?', reply_markup=start_keyboard())


def register_handlers_lot_creating(dp: Dispatcher):
    dp.register_callback_query_handler(lot_creating_start, lambda call: call.data == 'create_lot', state="*")
    dp.register_message_handler(title_chosen, state=CreateLot.waiting_for_lot_title)
    dp.register_message_handler(lot_price_chosen, state=CreateLot.waiting_for_lot_price)
    dp.register_message_handler(lot_description_chosen, state=CreateLot.waiting_for_lot_description)
    dp.register_message_handler(lot_category_chosen, state=CreateLot.waiting_for_lot_category)
    dp.register_message_handler(lot_images_chosen, state=CreateLot.waiting_for_lot_images)
