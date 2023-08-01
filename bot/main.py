# для ф-ии start_bot and _on_start_up
import os

from aiogram import Bot, executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

from handlers.admin.ahandlers import *
from handlers.user.uhandlers import echo

# забираем токен из .env
load_dotenv()
TOKEN = os.getenv('API_KEY')


def start_bot():
    """ф-ия для инициализации bot dp и запуска через executor"""
    my_storage = MemoryStorage()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot, storage=my_storage)

    # админские диспетчеры
    dp.register_message_handler(hide_command, commands=['hide'])
    dp.register_message_handler(admin_signin, Text(equals='Вход'), state=AdminStatesGroup.hide_field)
    dp.register_message_handler(enter_login, state=AdminStatesGroup.enter_login)
    dp.register_message_handler(enter_password, state=AdminStatesGroup.enter_password)

    dp.register_message_handler(echo)

    executor.start_polling(dp, skip_updates=True)
