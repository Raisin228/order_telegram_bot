# для ф-ии start_bot and _on_start_up
import os

from aiogram import Bot, executor, Dispatcher
from dotenv import load_dotenv

from handlers.user.uhandlers import *
from order_telegram_bot.sqlite_bot.sqlite import *


# забираем токен из .env
load_dotenv()
TOKEN = os.getenv('API_KEY')


# запуск базы данных(создание)
# async def on_startup(_):
#     await db_start()


# ф-ия для инициализации bot dp и запуска через executor
def start_bot():
    global bot
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
    db_start()
    # команда /start для обычного пользователя
    dp.register_message_handler(start_user_cmd, commands=['start'])

    # команда /help для обычного пользователя
    dp.register_message_handler(help_user_cmd, commands=['help'])

    # команда /desc (описание бота) для обычного пользователя
    dp.register_message_handler(description_cmd, commands=['desc'])

    # команда для получения ближайших событий
    dp.register_message_handler(get_events, commands=['События'])

    executor.start_polling(dp, skip_updates=True)