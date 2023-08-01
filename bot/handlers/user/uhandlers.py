from aiogram import types
from order_telegram_bot.bot.config import *
from order_telegram_bot.bot.keyboards.user.replykb import *
from order_telegram_bot.sqlite_bot.sqlite import *
# обработчики команд


# команда /start
async def start_user_cmd(message: types.Message):
    await message.answer(text=START_USER_TEXT, reply_markup=user_keyboard())


# команда /help
async def help_user_cmd(message: types.Message):
    await message.answer(text=HELP_USER_TEXT)


# команда /desc
async def description_cmd(message: types.Message):
    await message.answer(text=DESCRIPTION_USER)


# команда "Что будет?"
async def get_events(message: types.Message):
    # список событий, с датой не далее, чем за 7 дней от текущей
    data_events = week_events()
    if data_events:
        await message.answer(text='Вот все мероприятия на ближайшие 7 дней!')
    else:
        await message.answer(text='Событий пока нет, но они обязательно появятся!')
    for i in data_events:
        #await message.answer_photo(i[1], caption=f'{i[2]}\n{i[3]}')
        await message.answer(text=f'{i[2]}\n{i[3]}')
