# reply kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def login_vs_signin() -> ReplyKeyboardMarkup:
    """Создаём клавиатуру для входа админа"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Вход')
    kb.add(button1)
    return kb
