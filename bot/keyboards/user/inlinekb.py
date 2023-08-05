from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def inline_basket_keyboard(count_product=1) -> InlineKeyboardMarkup:
    """Inline клавиатура для добавления продуктов в корзину"""
    ikb = InlineKeyboardMarkup()

    ib_1 = InlineKeyboardButton(text='+', callback_data=f'+ {count_product}')
    ib_2 = InlineKeyboardButton(text=f'{count_product}', callback_data='1')
    ib_3 = InlineKeyboardButton(text='-', callback_data=f'- {count_product}')
    ib_4 = InlineKeyboardButton(text='В корзину', callback_data=f'{count_product}')
    ikb.row(ib_1, ib_2, ib_3)
    ikb.add(ib_4)
    return ikb


def inline_product_keyboard(product_data) -> InlineKeyboardMarkup:
    """Клавиатура для редактирования кол-ва продукта в корзине"""
    ikb = InlineKeyboardMarkup()

    ib_1 = InlineKeyboardButton(text='+', callback_data=f'B + {product_data[0]}')
    ib_2 = InlineKeyboardButton(text=f'{product_data[1]}', callback_data='1')
    ib_3 = InlineKeyboardButton(text='-', callback_data=f'B - {product_data[0]}')
    ikb.add(ib_1, ib_2, ib_3)
    return ikb
