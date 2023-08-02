from aiogram import types
from aiogram.dispatcher import FSMContext

from order_telegram_bot.bot.config import *
from order_telegram_bot.bot.keyboards.user.replykb import *
from order_telegram_bot.sqlite_bot.sqlite import *
from order_telegram_bot.bot.handlers.user.user_states import UserMenuStatesGroup
# обработчики команд пользователя


async def start_user_cmd(message: types.Message):
    """Обработчик команды /start"""

    # ВРЕМЕННО
    await create_event()
    await create_menu()

    await message.answer(text=START_USER_TEXT, reply_markup=user_start_keyboard())


async def help_user_cmd(message: types.Message):
    """Обработчик команды /help"""
    await message.answer(text=HELP_USER_TEXT)


async def description_cmd(message: types.Message):
    """Обработчик команды /desk(описание бота)"""
    await message.answer(text=DESCRIPTION_USER)


async def get_events(message: types.Message):
    """Обработчик команды 'Что будет?' для получения событий на ближайшие 7 дней"""
    data_events = week_events()
    if data_events:
        await message.answer(text='Вот все мероприятия на ближайшие 7 дней!')
    else:
        await message.answer(text='Событий пока нет, но они обязательно появятся!')
    # вывод событий
    for i in data_events:
        #await message.answer_photo(i[1], caption=f'{i[2]}\n{i[3]}')
        # ВРЕМЕННЫЙ ВАРИАНТ СООБЩЕНИЯ БЕЗ ФОТО
        await message.answer(text=f'{i[2]}\n{i[3]}')


async def get_menu_position(message: types.Message):
    """Отправка пользователю карточки меню"""
    await UserMenuStatesGroup.viewing_menu.set()
    await message.answer(text='Выберите понравившийся бургер, чтобы узнать о нем подробнее!',
                         reply_markup=user_menu_keyboard())


async def choice_position_menu(message: types.Message, state: FSMContext):
    """Пользователь выбирает позицию меню"""

    # действия при нажатии кнопки выхода
    if message.text.lower() == 'вернуться':
        await message.answer(text='Вы в главном меню!', reply_markup=user_start_keyboard())
        await state.finish()
    else:
        # словарь с данными о продуктах(ключ - название продукта)
        menu_dict = menu_positions()
        await UserMenuStatesGroup.viewing_menu.set()
        # await message.answer_photo(menu_dict[message.text][0], caption=f'{message.text}\n'
        #                                                                f'{menu_dict[message.text][1]}\n'
        #                                                                f'Стоимость: {menu_dict[message.text][2]}')
        # ВРЕМЕННЫЙ ВАРИАНТ СООБЩЕНИЯ БЕЗ ФОТО
        await message.answer(text=f'{message.text}\n'
                                  f'{menu_dict[message.text][1]}\n'
                                  f'Стоимость: {menu_dict[message.text][2]}')
