from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# клавиатура для пользователя
def user_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    # кнопка получения событий
    b1 = KeyboardButton('/События')

    kb.row(b1)
    return kb

