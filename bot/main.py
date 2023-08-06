# для ф-ии start_bot and _on_start_up

from aiogram import executor, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from handlers.admin.ahandlers import *
from handlers.user.uhandlers import *
from order_telegram_bot.sqlite_bot.sqlite import *
from other import my_pred, is_good_link


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
    dp.register_message_handler(cancel, lambda m: m.text in ['Отмена', '🚪 Выйти из админ.панели'], state='*')
    dp.register_message_handler(in_main_menu, Text(equals='⬅️ В главное меню'), state='*')
    # =======================admin handlers=======================

    """Всё что касается регистрации и входа"""
    # вход в скрытое поле
    dp.register_message_handler(hide_command, commands=['hide'])

    # Регистрация нового админа
    dp.register_message_handler(admin_login, Text(equals='📝 Регистрация'), state=AdminStatesGroup.hide_field)

    # Запрос пароля при регистрации нового админа
    dp.register_message_handler(enter_new_password, state=AdminStatesGroup.enter_new_password)

    # подтверждение пароля админа если регистрируется 2 >= админов
    dp.register_message_handler(enter_pass_conf, state=AdminStatesGroup.enter_pass_conf)

    # вход в акк админа
    dp.register_message_handler(admin_signin, Text(equals='🔑 Вход'), state=AdminStatesGroup.hide_field)

    # ввод пароля
    dp.register_message_handler(enter_password, content_types=types.ContentType.TEXT,
                                state=AdminStatesGroup.enter_password)

    # обработчики неверных данных
    dp.register_message_handler(dont_correct, content_types=types.ContentType.ANY,
                                state=AdminStatesGroup.hide_field)
    dp.register_message_handler(dont_correct_password, content_types=types.ContentType.ANY,
                                state=[AdminStatesGroup.enter_password, AdminStatesGroup.enter_new_password,
                                       AdminStatesGroup.enter_pass_conf])

    """Создание новых событий"""
    # начало создание события
    dp.register_message_handler(adm_create_event, Text(equals='🎫 Создать мероприятие'),
                                state=AdminStatesGroup.adm_control_panel)

    # название + проверяем на корректность
    dp.register_message_handler(get_name_of_event, content_types=types.ContentType.TEXT, state=AdminStatesGroup.e_name)
    dp.register_message_handler(is_correct_name, content_types=types.ContentType.ANY,
                                state=AdminStatesGroup.e_name)

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
    dp.register_message_handler(get_photo_event, state=AdminStatesGroup.get_photo, content_types=['photo'])
    dp.register_message_handler(is_correct_photo, content_types=types.ContentType.ANY, state=AdminStatesGroup.get_photo)

    # если не нужна ссылка пропускаем данный этап
    dp.register_message_handler(dont_need_link, Text(equals='-'), state=AdminStatesGroup.get_link)
    # иначе получаем ссылку + минимальная проверка на корректность
    dp.register_message_handler(get_link_to_social_networks, lambda m: is_good_link(m.text),
                                content_types=types.ContentType.TEXT, state=AdminStatesGroup.get_link)
    dp.register_message_handler(is_correct_link, content_types=types.ContentType.ANY, state=AdminStatesGroup.get_link)

    # подтверждение правильно собранной анкеты
    dp.register_message_handler(show_ads, Text(equals='👁 Показать анкету'), state=AdminStatesGroup.ads_confirmation)

    # в случае если пользователь решил внести изменения
    dp.register_message_handler(change_ads, Text(equals='🤨 Хочу переделать :('),
                                state=AdminStatesGroup.ads_confirmation)

    # записали событие в бд
    dp.register_message_handler(add_ads_to_db, Text(equals='✅ Просто шикарно!!'), state=AdminStatesGroup.ads_confirmation)

    # защита от дурака
    dp.register_message_handler(dont_correct, content_types=types.ContentType.ANY,
                                state=AdminStatesGroup.ads_confirmation)

    """Изменение уже существующих событий"""
    # начало изменения события
    dp.register_message_handler(list_events_to_edit, Text(equals='✍️ Изменить календарь мероприятий'),
                                state=AdminStatesGroup.adm_control_panel)
    # редактируем|удаляем|отмена
    dp.register_message_handler(action_with_adv, state=AdminStatesGroup.choose_edit_advs)

    # перебрасываем пользователя на редактирование
    dp.register_message_handler(edit_exist_adv, Text(equals='🟠 Изменить'), state=AdminStatesGroup.edit_advs)

    # удаляем выбранный пост из бд
    dp.register_message_handler(permanent_del, Text(equals='🗑 Удалить'), state=AdminStatesGroup.edit_advs)

    """Бургеры"""
    # попадаем в ветку бургеров
    dp.register_message_handler(burgers_menu, Text(equals='🍔 Бургеры'), state=AdminStatesGroup.adm_control_panel)

    # начинаем добавление
    dp.register_message_handler(add_new_product, Text(equals='🟢 Добавить новый вид бургеров'),
                                state=AdminStatesGroup.burgers_menu)

    # название товара + проверка данных
    dp.register_message_handler(get_name_burger, state=AdminStatesGroup.name_new_product)
    dp.register_message_handler(is_correct_name, content_types=types.ContentType.ANY,
                                state=AdminStatesGroup.name_new_product)

    # фото еды + проверка
    dp.register_message_handler(get_burger_photo, state=AdminStatesGroup.get_photo_dish, content_types=['photo'])
    dp.register_message_handler(is_correct_photo, content_types=types.ContentType.ANY,
                                state=AdminStatesGroup.get_photo_dish)

    # описание еды + проверка на корректность
    dp.register_message_handler(get_descript_dish, state=AdminStatesGroup.dish_descript,
                                content_types=types.ContentType.TEXT)
    dp.register_message_handler(is_correct_desc, content_types=types.ContentType.ANY,
                                state=AdminStatesGroup.dish_descript)

    # устанавливаем цену на товар + проверка
    dp.register_message_handler(price, lambda m: all(map(str.isdigit, m.text)), state=AdminStatesGroup.dish_price,
                                content_types=types.ContentType.TEXT)
    dp.register_message_handler(is_correct_price, content_types=types.ContentType.ANY,
                                state=AdminStatesGroup.dish_price)

    # подтверждение правильно собранной фото карточки
    dp.register_message_handler(show_dish, Text(equals='👁 Показать фото-карточку товара'),
                                state=AdminStatesGroup.dish_confirmation)

    # в случае если пользователь решил внести изменения
    dp.register_message_handler(change_dish, Text(equals='🤨 Хочу переделать :('),
                                state=AdminStatesGroup.dish_confirmation)

    # записали новый товар в бд
    dp.register_message_handler(add_dish_to_db, Text(equals='✅ Просто шикарно!!'),
                                state=AdminStatesGroup.dish_confirmation)

    """Изменение товаров в меню"""
    # начало изменения события
    dp.register_message_handler(list_dishes_to_edit, Text(equals='✏️ Редактировать текущее меню'),
                                state=AdminStatesGroup.burgers_menu)
    # редактируем|удаляем|отмена
    dp.register_message_handler(action_with_dish, state=AdminStatesGroup.choose_edit_dish)

    # перебрасываем пользователя на редактирование
    dp.register_message_handler(edit_exist_dish, Text(equals='🟠 Изменить'), state=AdminStatesGroup.edit_dish)

    # удаляем выбранный пост из бд
    dp.register_message_handler(permanent_del_dish, Text(equals='🗑 Удалить'), state=AdminStatesGroup.edit_dish)

    # защита от дурака
    dp.register_message_handler(dont_correct, content_types=types.ContentType.ANY,
                                state=[AdminStatesGroup.adm_control_panel, AdminStatesGroup.edit_advs,
                                       AdminStatesGroup.burgers_menu, AdminStatesGroup.dish_confirmation,
                                       AdminStatesGroup.choose_edit_advs, AdminStatesGroup.choose_edit_dish,
                                       AdminStatesGroup.edit_dish])

    # =======================user handlers=======================
    # команда /start для обычного пользователя
    dp.register_message_handler(start_user_cmd, commands=['start'])

    # команда /help для обычного пользователя
    dp.register_message_handler(help_user_cmd, commands=['help'])

    # команда /desc (описание бота) для обычного пользователя
    dp.register_message_handler(description_cmd, commands=['desc'])

    # команда для получения ближайших событий
    dp.register_message_handler(get_events, Text(equals='📑 Список ближайших мероприятий', ignore_case=True))

    # команда для перехода в меню
    dp.register_message_handler(get_menu_position, Text(equals='📕 Меню', ignore_case=True))

    # состояние выбора позиций меню
    dp.register_message_handler(choice_position_menu, state=UserMenuStatesGroup.viewing_menu)

    # ответ на нажатие inline кнопки
    dp.register_callback_query_handler(callback_add_basket)

    # обработчик выхода из меню (если пользователь ничего не выбрал)
    dp.register_message_handler(back_menu_cmd, Text(equals='⬅️ Вернуться', ignore_case=True))

    # обработчик команды возврата в меню
    dp.register_message_handler(back_in_menu_cmd, Text(equals='⬅️ Вернуться в меню', ignore_case=True))

    # обработчик выхода в корзину
    dp.register_message_handler(viewing_basket_cmd, Text(startswith='🛍 Корзина', ignore_case=True))

    # обработчик очистки корзины
    dp.register_message_handler(clear_basket_cmd, Text(equals='🗑 Очистить всю корзину', ignore_case=True))

    # обработчик для оформления заказа
    dp.register_message_handler(start_order_cmd, Text(equals='🎁 Заказать', ignore_case=True))

    # обработчик команды для отмены заполнения заказа
    dp.register_message_handler(cancel_order_cmd, Text(equals='❌ Отменить заказ', ignore_case=True), state='*')

    # обработчик состояния ввода адреса
    dp.register_message_handler(enter_address_step, state=UserMenuStatesGroup.enter_address)

    # обработчик для выбора способа оплаты
    dp.register_message_handler(payment, state=UserMenuStatesGroup.choice_payment)

    # проверка перед оплатой
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda query: True)

    # ответ на успешный платеж
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)

    # отправка стикера на стикер
    dp.register_message_handler(send_sticker, content_types='sticker', state='*')

    # бот не понял сообщение
    dp.register_message_handler(dont_understend, content_types=types.ContentType.ANY, state='*')

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
