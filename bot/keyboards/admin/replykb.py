# reply kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def cancelkb() -> ReplyKeyboardMarkup:
    """Сброс в самое главное меню"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Отмена')
    kb.add(button1)
    return kb


def login_vs_signin() -> ReplyKeyboardMarkup:
    """Создаём клавиатуру для входа админа"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Вход')
    button2 = KeyboardButton('Регистрация')
    kb.add(button1, button2)
    return kb


def adm_opportunities() -> ReplyKeyboardMarkup:
    """Кнопки с дейстиями админа"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Создать мероприятие')
    button2 = KeyboardButton('Изменить календарь мероприятий')
    button3 = KeyboardButton('Меню бургеров')
    kb.add(button1).add(button2, button3)
    return kb


def adm_get_do_post() -> ReplyKeyboardMarkup:
    """Клавиатура для получения только что заполненных данных объявления"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Показать анкету')
    kb.add(button1)
    return kb


def right_anket() -> ReplyKeyboardMarkup:
    """Подтверждение правильно введённой анкеты"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Просто шикарно!!')
    button2 = KeyboardButton('Хочу переделать :(')
    kb.add(button1, button2)
    return kb
