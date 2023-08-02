# сами обработчики администратора
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from order_telegram_bot.bot.config import *
from order_telegram_bot.bot.handlers.admin.admi_states import AdminStatesGroup
from order_telegram_bot.bot.keyboards.admin.replykb import *
from order_telegram_bot.sqlite_bot.sqlite import quantity_admins, create_admin, chose_admin_password, get_user_password


async def hide_command(message: types.Message) -> None:
    """Обработчик того что user зашёл в скрытое поле регистрации"""
    await message.answer(ADM_CMD_HIDE, reply_markup=login_vs_signin())
    # теперь бот находится в состоянии скрытого поля регистрации
    await AdminStatesGroup.hide_field.set()
    await message.delete()


async def admin_login(message: types.Message) -> None:
    """Регистрация нового администратора в боте"""
    if not quantity_admins():
        await message.answer(IMAG_NEW_PASS, reply_markup=ReplyKeyboardRemove())
        await AdminStatesGroup.enter_new_password.set()
    else:
        # перед тем как регистрировать пользователя проверяем что он ещё не админ
        if get_user_password(message.from_user.id) is None:
            await message.answer(ADM_ALRADY_HAVE, reply_markup=ReplyKeyboardRemove())
            await AdminStatesGroup.enter_pass_conf.set()
        else:
            await message.answer(ADM_RE_REGISTR)


async def enter_pass_conf(message: types.Message):
    """Проверка пароля 1 администратора чтобы зарегать 2 админа"""
    if await chose_admin_password() == message.text:
        await message.answer(CORRECT_PASS)
        await message.answer(IMAG_NEW_PASS)
        await AdminStatesGroup.enter_new_password.set()
    else:
        await message.answer(UNCORECT_PASS, reply_markup=cancelkb())


async def enter_new_password(message: types.Message):
    """Запрос пароля при регистрации нового админа"""
    if await create_admin(message.from_user.id, message.text) is not None:
        await message.answer(YOU_ADM, reply_markup=login_vs_signin())
        await AdminStatesGroup.hide_field.set()
    else:
        await message.answer(ADM_RE_REGISTR, reply_markup=login_vs_signin())
        await AdminStatesGroup.hide_field.set()


async def admin_signin(message: types.Message) -> None:
    """
    На данном этапе пользователь находится в скрытом
    после нажатия кнопки Вход
    """
    await message.answer(ADM_SIGNIN,
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(ENTER_PASS)
    await AdminStatesGroup.enter_password.set()


async def cancel(message: types.Message, state: FSMContext) -> None:
    """Кнопка canel для выхода в самое главное меню"""
    await state.finish()
    await message.answer('Вы вышли в главное меню user', reply_markup=ReplyKeyboardRemove())


async def enter_password(message: types.Message, state: FSMContext) -> None:
    """
    User вводит пароль. Мы сверяем его с password из бд
    """
    param = get_user_password(message.from_user.id)
    if param is None:
        await message.answer(DONT_ADM)
    elif message.text == param:
        await message.answer(ADM_CONF_PASS)
        await state.finish()
    else:
        await message.answer(UNCORECT_PASS, reply_markup=cancelkb())
