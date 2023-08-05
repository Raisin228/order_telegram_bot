# inline kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def link_in_button_adv(link: str) -> InlineKeyboardMarkup:
    """Кнопка с сылкой на мероприятие"""
    kb = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='Ссылка', url=link)
    kb.add(button)
    return kb
