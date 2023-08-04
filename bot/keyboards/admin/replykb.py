# reply kb
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def exit_kb() -> ReplyKeyboardMarkup:
    """выход в главное меню admin"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('В главное меню'))
    return kb


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
    button3 = KeyboardButton('Бургеры')
    button4 = KeyboardButton('Выйти из админ.панели')
    kb.add(button1).add(button2, button3).add(button4)
    return kb


def get_do_post(text: str) -> ReplyKeyboardMarkup:
    """Клавиатура для получения только что заполненных данных объявления/товара"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text)
    kb.add(button1)
    return kb


def right_anket() -> ReplyKeyboardMarkup:
    """Подтверждение правильно введённых данных"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Просто шикарно!!')
    button2 = KeyboardButton('Хочу переделать :(')
    kb.add(button1, button2)
    kb.add(KeyboardButton('В главное меню'))
    return kb


def view_events(data: list) -> ReplyKeyboardMarkup:
    """Показать кнопки с названиями мероприятий/товаров"""
    kb = ReplyKeyboardMarkup()
    # делаем очень много кнопок со всеми событиями
    for i in data:
        button = KeyboardButton(f'{i[0]} {i[1]}  {i[2]}')
        kb.insert(button)
    kb.add('В главное меню')
    return kb


def del_or_edit() -> ReplyKeyboardMarkup:
    """Клавиатура для изменение мероприятия"""
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = KeyboardButton('Изменить')
    but2 = KeyboardButton('Удалить')
    but3 = KeyboardButton('В главное меню')
    kb.add(but1, but2).add(but3)
    return kb


def new_prod_or_edit_exist() -> ReplyKeyboardMarkup:
    """Редактирование/ добавление товаров в меню"""
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Добавить новый вид бургеров'),
                                                         KeyboardButton('Редактировать текущее меню')).add(
        KeyboardButton('В главное меню'))


