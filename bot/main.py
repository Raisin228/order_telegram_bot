# для ф-ии start_bot and _on_start_up

from aiogram import Bot, executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType


from handlers.admin.ahandlers import *
from handlers.user.uhandlers import *
from order_telegram_bot.sqlite_bot.sqlite import *
from other import my_pred


async def on_startup(_):
    """Запуск базы данных (создание)"""
    db_start()


bot = Bot(token=TOKEN)


def start_bot():
    """ф-ия для инициализации bot dp и запуска через executor"""
    global bot
    my_storage = MemoryStorage()
    dp = Dispatcher(bot, storage=my_storage)

    # самая главная кнопка отмены
    dp.register_message_handler(cancel, Text(equals='Отмена'), state='*')

    # =======================admin handlers=======================

    """Всё что касается регистрации и входа"""
    # вход в скрытое поле
    dp.register_message_handler(hide_command, commands=['hide'])

    # Регистрация нового админа
    dp.register_message_handler(admin_login, Text(equals='Регистрация'), state=AdminStatesGroup.hide_field)

    # Запрос пароля при регистрации нового админа
    dp.register_message_handler(enter_new_password, state=AdminStatesGroup.enter_new_password)

    # подтверждение пароля админа если регистрируется 2 >= админов
    dp.register_message_handler(enter_pass_conf, state=AdminStatesGroup.enter_pass_conf)

    # вход в акк админа
    dp.register_message_handler(admin_signin, Text(equals='Вход'), state=AdminStatesGroup.hide_field)

    # ввод пароля
    dp.register_message_handler(enter_password, state=AdminStatesGroup.enter_password)

    """События"""
    # начало создание события
    dp.register_message_handler(adm_create_event, Text(equals='Создать мероприятие'),
                                state=AdminStatesGroup.adm_control_panel)

    # название + проверяем на корректность
    dp.register_message_handler(get_name_of_event, content_types=types.ContentType.TEXT, state=AdminStatesGroup.e_name)
    dp.register_message_handler(is_correct_name, content_types=types.ContentType.ANY, state=AdminStatesGroup.e_name)

    # дата + проверяем на корректность
    dp.register_message_handler(get_date_of_event, lambda mes: my_pred(mes.text),
                                content_types=types.ContentType.TEXT, state=AdminStatesGroup.e_date)
    dp.register_message_handler(is_correct_date, content_types=types.ContentType.ANY,
                                state=AdminStatesGroup.e_date)

    # описание + проверяем на корректность
    dp.register_message_handler(get_descript_event, state=AdminStatesGroup.e_descript,
                                content_types=types.ContentType.TEXT)
    dp.register_message_handler(is_correct_desc, content_types=types.ContentType.ANY, state=AdminStatesGroup.e_descript)

    # получение фотки + проверка
    dp.register_message_handler(get_photo_event, state=AdminStatesGroup.e_photo, content_types=['photo'])
    dp.register_message_handler(is_correct_photo, content_types=types.ContentType.ANY, state=AdminStatesGroup.e_photo)

    # подтверждение правильно собранной анкеты
    dp.register_message_handler(show_ads, Text(equals='Показать анкету'), state=AdminStatesGroup.ads_confirmation)

    # в случае если пользователь решил внести изменения
    dp.register_message_handler(change_ads, Text(equals='Хочу переделать :('),
                                state=AdminStatesGroup.ads_confirmation)

    # записали событие в бд
    dp.register_message_handler(add_ads_to_db, Text(equals='Просто шикарно!!'), state=AdminStatesGroup.ads_confirmation)

    # =======================user handlers=======================
    # команда /start для обычного пользователя
    dp.register_message_handler(start_user_cmd, commands=['start'])

    # команда /help для обычного пользователя
    dp.register_message_handler(help_user_cmd, commands=['help'])

    # команда /desc (описание бота) для обычного пользователя
    dp.register_message_handler(description_cmd, commands=['desc'])

    # команда для получения ближайших событий
    dp.register_message_handler(get_events, Text(equals='Что будет?', ignore_case=True))

    # команда для перехода в меню
    dp.register_message_handler(get_menu_position, Text(equals='Меню', ignore_case=True))

    # состояние выбора позиций меню
    dp.register_message_handler(choice_position_menu, state=UserMenuStatesGroup.viewing_menu)

    # ответ на нажатие inline кнопки
    dp.register_callback_query_handler(callback_add_basket)

    # обработчик выхода из меню (если пользователь ничего не выбрал)
    dp.register_message_handler(back_menu_cmd, Text(equals='Вернуться', ignore_case=True))

    # обработчик команды возврата в меню
    dp.register_message_handler(back_in_menu_cmd, Text(equals='Вернуться в меню', ignore_case=True))

    # обработчик выхода в корзину
    dp.register_message_handler(viewing_basket_cmd, Text(startswith='Корзина', ignore_case=True))

    # обработчик очистки корзины
    dp.register_message_handler(clear_basket_cmd, Text(equals='Очистить всю корзину', ignore_case=True))

    # обработчик для оформления заказа
    dp.register_message_handler(start_order_cmd, Text(equals='Заказать', ignore_case=True))

    # обработчик команды для отмены заполнения заказа
    dp.register_message_handler(cancel_order_cmd, Text(equals='Отменить заказ', ignore_case=True), state='*')

    # обработчик состояния ввода адреса
    dp.register_message_handler(enter_address_step, state=UserMenuStatesGroup.enter_address)

    # обработчик для выбора способа оплаты
    dp.register_message_handler(payment, state=UserMenuStatesGroup.choice_payment)

    # проверка перед оплатой
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda query: True)

    # ответ на успешный платеж
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
