from aiogram import types


def start_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Смотреть все объявления", callback_data="view_lots"))
    keyboard.add(types.InlineKeyboardButton(text="Мои объявления", callback_data="user_lots"))
    keyboard.add(types.InlineKeyboardButton(text="Создать объявление", callback_data="create_lot"))
    keyboard.add(types.InlineKeyboardButton(text="Объявления по категориям", callback_data="watch_by_categories"))
    return keyboard
