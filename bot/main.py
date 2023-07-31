# для ф-ии start_bot and _on_start_up
import os

from aiogram import Bot, executor, Dispatcher
from dotenv import load_dotenv

from handlers.user.uhandlers import echo

# забираем токен из .env
load_dotenv()
TOKEN = os.getenv('API_KEY')


# ф-ия для инициализации bot dp и запуска через executor
def start_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)

    dp.register_message_handler(echo)

    executor.start_polling(dp, skip_updates=True)