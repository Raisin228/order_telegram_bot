import os
from random import choice

import aiogram.utils.exceptions
from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

from order_telegram_bot.bot.config import *
from order_telegram_bot.bot.handlers.user.user_states import UserMenuStatesGroup
from order_telegram_bot.bot.keyboards.user.inlinekb import *
from order_telegram_bot.bot.keyboards.user.replykb import *

from order_telegram_bot.sqlite_bot.sqlite import *
from order_telegram_bot.bot.other import *

# забираем токены из .env
load_dotenv()
TOKEN = os.getenv('API_KEY')
PAY_TOKEN = os.getenv('PAY_TOKEN')
GEO_TOKEN = os.getenv('YANDEX_GEO_TOKEN')
bot = Bot(token=TOKEN)


# обработчики команд пользователя


async def start_user_cmd(message: types.Message):
    """Обработчик команды /start"""
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEJ7ytkz0X-9bZnxbLmTShkDPl8bl-UtQAC2A8AAkjyYEsV-8TaeHRrmC8E')
    await message.answer(text=START_USER_TEXT, parse_mode='html',
                         reply_markup=user_start_keyboard(message.from_user.id))


async def help_user_cmd(message: types.Message):
    """Обработчик команды /help"""
    await message.answer(text=HELP_USER_TEXT, parse_mode='html')


async def description_cmd(message: types.Message):
    """Обработчик команды /desk(описание бота)"""
    await message.answer(text=DESCRIPTION_USER, parse_mode='html')


async def get_events(message: types.Message):
    """Обработчик команды 'Что будет?' для получения событий на ближайшие 7 дней"""
    data_events = week_events()
    if data_events:
        await message.answer(text=EVENTS_7DAYS, parse_mode='html')
    else:
        await message.answer(text=NO_EVENTS)
    # вывод событий
    for i in data_events:
        if i[5] == '-':
            await message.answer_photo(i[2], caption=f'{i[1]}\n{i[3]}\n{i[4]}')
        else:
            await message.answer_photo(i[2], caption=f'{i[1]}\n{i[3]}\n{i[4]}',
                                       reply_markup=inline_event_keyboard(i[5]))


async def get_menu_position(message: types.Message, state: FSMContext):
    """Отправка пользователю карточки меню"""
    if menu_positions():
        await UserMenuStatesGroup.viewing_menu.set()
        await message.answer(text=CHOOSE_BURGER,
                             reply_markup=user_menu_keyboard())
    else:
        await message.answer(text='В меню пока ничего нет', reply_markup=user_start_keyboard(message.from_user.id))
        await state.finish()


async def choice_position_menu(message: types.Message, state: FSMContext):
    """Пользователь выбирает позицию меню"""

    # действия при нажатии кнопки выхода
    if message.text.lower() == '⬅️ вернуться':
        await state.finish()
        await message.answer(text='Вы в главном меню!', reply_markup=user_start_keyboard(message.from_user.id))
    else:
        await state.finish()
        # словарь с данными о продуктах(ключ - название продукта)
        menu_dict = menu_positions()

        await message.delete()
                         
        try:
            await message.answer(text='Хороший выбор!👍', reply_markup=user_menu_position())
            await message.answer_photo(menu_dict[message.text][0], caption=f'<b>Название:</b> {message.text}\n'
                                       f'<b>Описание:</b>{menu_dict[message.text][1]}\n'
                                       f'<b>Стоимость:</b> {menu_dict[message.text][2]}', parse_mode='html',
                                       reply_markup=inline_basket_keyboard())
        except KeyError:
            await message.answer(text='Такого блюда у нас нет(')


async def back_menu_cmd(message: types.Message):
    """Обработчик выхода в главное меню"""
    await message.answer(text='Вы в главном меню!', reply_markup=user_start_keyboard(message.from_user.id))


async def back_in_menu_cmd(message: types.Message):
    """Обработчик возврата в продуктовое меню"""
    await UserMenuStatesGroup.viewing_menu.set()
    await message.answer(text='Вы находитесь в меню наших бургеров!', reply_markup=user_menu_keyboard())


async def callback_add_basket(callback: types.CallbackQuery):
    """Действия при нажатии inline кнопки"""
    data = callback.data
    # обработка callback данных
    # обработка данных для клавиатуры внутри корзины
    if data.split()[0] == 'B':
        if data.split()[1] == '+':
            product_data = add_basket(callback.from_user.id, ' '.join(data.split()[2:]))
            await callback.message.edit_reply_markup(reply_markup=inline_product_keyboard(product_data=product_data))

        if data.split()[1] == '-':
            product_data = add_basket(callback.from_user.id, data.split()[2], type_add='-')
            try:
                await callback.message.edit_reply_markup(
                    reply_markup=inline_product_keyboard(product_data=product_data))
            except aiogram.utils.exceptions.MessageNotModified:
                await callback.answer()
        # бездействие при нажатии на счетчик
        if data == 'count':
            await callback.answer()
    else:
        # обработка данных для клавиатуры в позиции меню
        # если решили увеличить кол-во
        if data.split()[0] == '+':
            await callback.message.edit_reply_markup(reply_markup=inline_basket_keyboard(count_product=int(
                data.split()[1]) + 1))
        # если решили уменьшить кол-во
        elif data.split()[0] == '-':
            # проверка на то, чтобы при уменьшении не уходить < 0
            if data.split()[1] != '1':
                await callback.message.edit_reply_markup(reply_markup=inline_basket_keyboard(count_product=int(
                    data.split()[1]) - 1))
            else:
                await callback.answer()
        # бездействие при нажатии на счетчик
        elif data == 'count':
            await callback.answer()
        else:
            # отправка данных в БД
            for i in range(int(data)):
                product_data = add_basket(callback.from_user.id,
                                          ' '.join(callback.message.caption.split('\n')[0].split()[1:]))
            await callback.answer(text='Товар добавлен в корзину!')


async def viewing_basket_cmd(message: types.Message):
    """Обработчик команды просмотра содержимого корзины"""
    await message.delete()
    data = get_basket_data(message.from_user.id)
    if data:
        if type(data[1]) == dict:
            product_names = list(data[1].keys())

            if product_names[0]:
                await message.answer(text='В вашей корзине сейчас:', reply_markup=edit_basket_keyboard())
                product_count = data[1]
                menu_dict = menu_positions()

                for product in product_count:
                    await message.answer(text=f'{product} - {menu_dict[product][2]}руб/шт.',
                                         reply_markup=inline_product_keyboard([product, product_count[product][0]]))
            else:
                await message.answer(text='Ваша корзина пуста')
        else:
            await message.answer(text='Ваша корзина пуста')
    else:
        await message.answer(text='Ваша корзина пуста')


async def clear_basket_cmd(message: types.Message):
    """Обработчик команды для полной очистки корзины"""
    res_delete = clear_basket(message.from_user.id)
    if res_delete:
        await message.answer(text='Ваша корзина уже пуста', reply_markup=user_start_keyboard(message.from_user.id))
    else:
        await message.answer(text='Ваша корзина очищена', reply_markup=user_start_keyboard(message.from_user.id))


async def cancel_order_cmd(message: types.Message, state: FSMContext):
    """Отмена заполнения заказа"""
    await message.answer(text='Заказ отменен', reply_markup=edit_basket_keyboard())
    await state.finish()


async def start_order_cmd(message: types.Message):
    """Обработчик команды для оформления заказа"""
    check_basket = get_basket_data(message.from_user.id)
    # проверка на пустоту корзины перед заказом
    if type(check_basket[1]) == dict:
        if check_basket[3]:
            await message.answer(text=f'Оставить прежний адрес?\n{check_basket[3]}', reply_markup=choice_keyboard())
            await UserMenuStatesGroup.choice_address.set()
        else:
            await message.answer(text=ADDRESS, reply_markup=user_order_cancel())
            await UserMenuStatesGroup.enter_address.set()
    else:
        await message.answer(text=IMPOSSIBLE_TO_ORDER,
                             reply_markup=user_start_keyboard(message.from_user.id))


async def address(message: types.Message):
    """Оставляем старый адрес или делаем новый"""
    if message.text.lower() == 'да':
        bd_num_phone = get_basket_data(message.from_user.id)[4]
        if bd_num_phone:
            await message.answer(text=f'Это ваш номер телефона: {bd_num_phone}?', reply_markup=choice_keyboard())
            await UserMenuStatesGroup.choice_phone.set()
    else:
        await message.answer(text=ADDRESS,
                             reply_markup=user_order_cancel())
        await UserMenuStatesGroup.enter_address.set()


async def enter_address_step(message: types.Message):
    """Обработчик ввода адреса для доставки"""
    # проверка адреса на корректность
    check = check_address(message.text, GEO_TOKEN)
    bd_num_phone = get_basket_data(message.from_user.id)[4]
    if not check:
        write_address(message.from_user.id, message.text)
        if bd_num_phone:
            await message.answer(text=f'Это ваш номер телефона: {bd_num_phone}?', reply_markup=choice_keyboard())
            await UserMenuStatesGroup.choice_phone.set()

        else:
            await message.answer(text='Введите ваш номер телефона')
            await UserMenuStatesGroup.user_phone.set()

    else:
        await message.answer(text=DONT_CORRECT_ADDRESS)
        await UserMenuStatesGroup.enter_address.set()


async def phone(message: types.Message):
    """Выбор телефона пользователя"""
    if message.text.lower() == 'да':
        await message.answer(text='Отлично! теперь выберете способ оплаты', reply_markup=user_payment_keyboard())
        await UserMenuStatesGroup.choice_payment.set()
    elif message.text.lower() == 'нет':
        await message.answer(text='Тогда введите новый номер телефона', reply_markup=user_order_cancel())
        await UserMenuStatesGroup.user_phone.set()
    else:
        await message.answer(text='Не понимаю вашего ответа(')
        await UserMenuStatesGroup.choice_phone.set()


async def get_user_phone(message: types.Message):
    """Получение номера телефона пользователя"""
    if phone_check(message.text):
        write_phone(message.from_user.id, message.text)
        await message.answer('Отлично! теперь выберете способ оплаты', reply_markup=user_payment_keyboard())
        await UserMenuStatesGroup.choice_payment.set()
    else:
        await message.answer('Введен не корректный номер телефона! Попробуйте еще раз')
        await UserMenuStatesGroup.user_phone.set()


async def payment(message: types.Message, state: FSMContext):
    """Обработчик выбора способа оплаты"""
    # формирование сообщения с итоговым заказом
    order_str = str()
    basket_data = get_basket_data(message.from_user.id)
    products = basket_data[1]

    # добавление информации о продуктах в итоговое сообщение
    for product in products:
        order_str += f'{product} - {products[product][0]}шт - {products[product][1]}руб.\n'
    # добавление информации об адресе
    order_str += f'Адрес доставки:\n{basket_data[3]}\n'

    if message.text.lower() == '💳 картой':
        await state.finish()

        # цена
        price = types.LabeledPrice(label='Оплата заказа', amount=basket_data[2] * 100)
        # отправка информации о заказе
        try:
            await message.answer(text='Заказ готов к оплате', reply_markup=user_order_cancel())
            await message.bot.send_invoice(message.from_user.id,
                                           title=f'Заказ для {message.from_user.username}',
                                           description=order_str,
                                           provider_token=PAY_TOKEN,
                                           currency='rub',
                                           prices=[price],
                                           start_parameter='order_pay',
                                           payload=f'user_{message.from_user.id}')
        except aiogram.utils.exceptions.BadRequest:
            await message.answer(text='Ошибка оформления заказа! Попробуйте изменить адрес доставки')
            await UserMenuStatesGroup.enter_address.set()

    elif message.text.lower() == '💵 наличными':
        order_str += f'\nИтог: {basket_data[2]}RUB'
        await message.answer(text='Заказ оформлен!')
        # очистка корзины при успешной оплате
        clear_basket(message.from_user.id)
        await message.answer(text='Ваш заказ:\n' + order_str, reply_markup=user_start_keyboard(message.from_user.id))
        await message.bot.send_message(chat_id=get_admin_id(), text=f'@{message.from_user.username} сделал заказ!\n'
                                                                    f'Заказ:\n{order_str}\nОплата наличными\n'
                                                                    f'Номер: {basket_data[4]}')
        await state.finish()
    else:
        await message.answer(DONT_CORRECT_PAYMENT)
        await UserMenuStatesGroup.choice_payment.set()


async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    """Проверка для осуществления оплаты"""
    # дается 10 секунд на подтверждение
    await pre_checkout_q.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


async def successful_payment(message: types.Message):
    """Обработчик успешного платежа"""

    # сообщение об успешной оплате для пользователя
    await message.answer(text=f'Заказ на сумму {message.successful_payment.total_amount // 100}'
                              f'{message.successful_payment.currency} успешно оплачен! Ожидайте!',
                         reply_markup=user_start_keyboard(message.from_user.id))

    # формирование сообщения с заказом для админа
    order_str = str()
    basket_data = get_basket_data(message.from_user.id)
    products = basket_data[1]

    for product in products:
        order_str += f'{product} - {products[product][0]}шт - {products[product][1]}руб.\n'

    order_str += f'Адрес доставки:\n{basket_data[3]}\n'
    order_str += f'\nИтог: {basket_data[2]}RUB'

    # сообщение об успешной оплате для главного админа
    await message.bot.send_message(chat_id=get_admin_id(), text=f'@{message.from_user.username} сделал заказ!\n'
                                                                f'Заказ:\n{order_str}\nОплачено картой\nНомер:'
                                                                f' {basket_data[4]}')
    # очистка корзины при успешной оплате
    clear_basket(message.from_user.id)


async def send_sticker(message: types.Message):
    """Отправляет случайный стикер пользователю в ответ на стикер"""
    await bot.send_sticker(message.chat.id, choice(list_stickers))


async def dont_understend(message: types.Message):
    """Заглушка на случай если пользователь ответил то что мы не предусмотрели"""
    await message.answer('Извините я Вас не понял 😥')
