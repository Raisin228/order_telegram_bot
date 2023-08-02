from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from order_telegram_bot.sqlite_bot.sqlite import menu_positions


def user_start_keyboard() -> ReplyKeyboardMarkup:
    """Начальная клавиатура пользователя"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    # кнопка получения событий
    b1 = KeyboardButton('Что будет?')
    b2 = KeyboardButton('Меню')

    kb.row(b1, b2)
    return kb


def user_menu_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура со списком продуктов"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = KeyboardButton('Вернуться')

    # получаем все названия продуктов меню
    menu_list = menu_positions().keys()
    for i in menu_list:
        kb.add(i)
    # добавляем кнопку возврата в главное меню
    kb.add(back_button)
    return kb
