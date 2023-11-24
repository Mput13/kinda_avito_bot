from aiogram import types


def start_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Ближайшие точки", callback_data="view_lots"))
    keyboard.add(types.InlineKeyboardButton(text="Интересные статьи", callback_data="create_lot"))
    return keyboard
