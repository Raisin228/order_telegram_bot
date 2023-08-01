# сами обработчики администратора
from aiogram import types

from order_telegram_bot.bot.config import ADM_CMD_HIDE, ADM_SIGNIN, ADM_CONF_LOG, ADM_CONF_PASS
from order_telegram_bot.bot.handlers.admin.admi_states import AdminStatesGroup
from order_telegram_bot.bot.keyboards.admin.replykb import *


async def hide_command(message: types.Message) -> None:
    """Обработчик того что user зашёл в скрытое поле регистрации"""
    await message.answer(ADM_CMD_HIDE, reply_markup=login_vs_signin())
    # теперь бот находится в состоянии скрытого поля регистрации
    await AdminStatesGroup.hide_field.set()
    await message.delete()


async def admin_signin(message: types.Message) -> None:
    """
    На данном этапе пользователь находится в скрытом
    после нажатия кнопки Вход
    """
    await message.answer(ADM_SIGNIN,
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('Введите Ваш логин: ')
    await AdminStatesGroup.enter_login.set()


async def enter_login(message: types.Message) -> None:
    """
    User ввёл логин. Мы делаем запрос в бд и проверяем что логин, который он ввёл соответствует сущ.
    -> в случае успеха переводим бота в состояние ожидания пароля
    """

    # временно пока нет бд админа
    login = 'abeb'

    # должен быть запрос в бд откуда я вытащу логин админа

    if message.text == login:
        await message.answer(ADM_CONF_LOG)
        await AdminStatesGroup.enter_password.set()
    else:
        await message.answer('Ошибка неверный логин')


async def enter_password(message: types.Message) -> None:
    """
    User вводит пароль. Мы сверяем его с password из бд
    """
    # временно пока нет бд админа
    password = '123'

    # должен быть запрос в бд откуда я вытащу пароль

    if message.text == password:
        await message.answer(ADM_CONF_PASS)
        await AdminStatesGroup.enter_password.set()
    else:
        await message.answer('Ошибка неверный пароль')
