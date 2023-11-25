from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from app.handlers.articles import articles
from keyboards import start_keyboard


class CreateLot(StatesGroup):
    article_name = State()


async def lot_creating_start(message: types.Message, state: FSMContext):
    keyboard = [[types.KeyboardButton(text=el)] for el in articles.keys()]
    await message.bot.send_message(message.from_user.id, "Выбирите название статьи",
                                   reply_markup=types.ReplyKeyboardMarkup(keyboard))
    await state.set_state(CreateLot.article_name.state)


async def title_chosen(message: types.Message, state: FSMContext):
    await message.answer(articles[message.text], reply_markup=start_keyboard())
    await state.finish()


def register_handlers_lot_creating(dp: Dispatcher):
    dp.register_callback_query_handler(lot_creating_start, lambda call: call.data == 'create_lot', state="*")
    dp.register_message_handler(title_chosen, state=CreateLot.article_name)
