# reply kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def login_vs_signin() -> ReplyKeyboardMarkup:
    """Создаём клавиатуру для входа админа"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Вход')
    button2 = KeyboardButton('Регистрация')
    kb.add(button1, button2)
    return kb


def cancelkb() -> ReplyKeyboardMarkup:
    """Сброс в самое главное меню"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Отмена')
    kb.add(button1)
    return kb
