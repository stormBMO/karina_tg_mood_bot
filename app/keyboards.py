from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

MAIN_MENU_BTNS = [["📝 Новая рефлексия"], ["🧘 Практики", "📊 Мои показатели"], ["📦 Экспорт записей"]]

def main_menu():
    b = ReplyKeyboardBuilder()
    for row in MAIN_MENU_BTNS:
        buttons = [KeyboardButton(text=text) for text in row]
        b.row(*buttons)
    return b.as_markup(resize_keyboard=True)
