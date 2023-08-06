from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from order_telegram_bot.sqlite_bot.sqlite import menu_positions, get_basket_data


def user_start_keyboard(user_id) -> ReplyKeyboardMarkup:
    """Начальная клавиатура пользователя"""
    try:
        price_in_basket = get_basket_data(user_id)[2]
    except TypeError:
        price_in_basket = 0

    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # кнопка получения событий
    b1 = KeyboardButton('📑 Список ближайших мероприятий')
    b2 = KeyboardButton('📕 Меню')
    b3 = KeyboardButton(f'🛍 Корзина {price_in_basket}руб.')

    kb.add(b1, b2, b3)

    return kb


def user_menu_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура со списком продуктов"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_button = KeyboardButton('⬅️ Вернуться')

    # получаем все названия продуктов меню
    menu_list = menu_positions().keys()
    for i in menu_list:
        kb.add(i)
    # добавляем кнопку возврата в главное меню
    kb.add(back_button)
    return kb


def user_menu_position() -> ReplyKeyboardMarkup:
    """Кнопка для возврата в меню"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    back_menu_bt = KeyboardButton('⬅️ Вернуться в меню')
    kb.add(back_menu_bt)
    return kb


def edit_basket_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для редактирования всей корзины"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    b1 = KeyboardButton('🗑 Очистить всю корзину')
    b2 = KeyboardButton('🎁 Заказать')
    b3 = KeyboardButton('⬅️ Вернуться')
    kb.add(b1, b2, b3)
    return kb


def user_order_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для оформления заказа"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Оплатить')
    b2 = KeyboardButton('❌ Отменить заказ')
    kb.add(b1, b2)
    return kb


def user_order_cancel() -> ReplyKeyboardMarkup:
    """Клавиатура для отмены заказа"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('❌ Отменить заказ')
    kb.add(button)
    return kb


def user_payment_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора способа оплаты"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('💳 Картой')
    b2 = KeyboardButton('💵 Наличными')
    b3 = KeyboardButton('❌ Отменить заказ')
    kb.row(b1, b2)
    kb.add(b3)
    return kb


def choice_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для выбора да/нет"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Да')
    b2 = KeyboardButton('Нет')
    b3 = KeyboardButton('❌ Отменить заказ')
    kb.row(b1, b2)
    kb.add(b3)
    return kb
