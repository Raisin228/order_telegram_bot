# сами обработчики администратора
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from order_telegram_bot.bot.config import *
from order_telegram_bot.bot.handlers.admin.admi_states import AdminStatesGroup
from order_telegram_bot.bot.keyboards.admin.inlinekb import link_in_button_adv
from order_telegram_bot.bot.keyboards.admin.replykb import *
from order_telegram_bot.bot.keyboards.user.replykb import user_start_keyboard
from order_telegram_bot.bot.main import bot
from order_telegram_bot.sqlite_bot.sqlite import quantity_admins, create_admin, \
    chose_admin_password, get_user_password, get_events_from_db, del_event_in_db, \
    create_menu, get_dishes_from_db, del_dish_in_db, write_event_to_db, get_admin_cafe_id, \
    get_all_admins, create_cafe_worker

"""Всякие обработчики отмены и возврата"""


async def cancel(message: types.Message, state: FSMContext) -> None:
    """Кнопка canel для выхода в самое главное меню user"""
    await state.finish()
    await message.answer(IN_USER_MENU, reply_markup=user_start_keyboard(message.chat.id))


async def step_back(message: types.Message) -> None:
    """Кнопка которая делает шаг назад"""
    await message.answer('Вы вернулись в главное меню /adm_actions', reply_markup=action_with_adm())
    await AdminStatesGroup.control_admins.set()


async def in_main_menu(message: types.Message) -> None:
    """Выход в гл. меню админа"""
    await AdminStatesGroup.adm_control_panel.set()
    await message.answer(IN_ADMIN_MENU, reply_markup=adm_opportunities())


"""Вход и регистрация"""


async def dont_correct(message: types.Message) -> None:
    """Говорим админу то что он ввёл не правильные данные на этапе hide_fiels"""
    await message.answer(DONT_CORRECT_DATA)


async def dont_correct_password(message: types.Message) -> None:
    """Говорим админу то что он ввёл не правильные данные на этапе enter_password"""
    await message.answer(TIPS_FOR_PASS)


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
    if await create_admin(user_id=message.from_user.id, user_name=message.from_user.first_name,
                          password=message.text) is not None:
        await message.answer(YOU_ADM, reply_markup=login_vs_signin())
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


async def enter_password(message: types.Message) -> None:
    """
    User вводит пароль. Мы сверяем его с password из бд
    """
    param = get_user_password(message.from_user.id)
    if param is None:
        await message.answer(DONT_ADM, reply_markup=cancelkb())
    elif message.text == param:
        await message.answer(ADM_CONF_PASS)
        # переводим админа в состояние панели админа + прикрепляем kb
        await message.answer(WHAT_U_WANR, reply_markup=adm_opportunities())
        await AdminStatesGroup.adm_control_panel.set()
    else:
        await message.answer(UNCORECT_PASS, reply_markup=cancelkb())


"""Работа в скрытом поле (редактирования прав для админов)"""


async def admin_actions_with_other_admins(message: types.Message) -> None:
    """Админ зашёл во 2-ое скрытое поле где он может редактировать список администраторов и выдавать им разные права
    (доступно только для главного администратора)"""

    # удаляем сообщение чтобы он не спамил
    await message.delete()
    # запрос в бд для того чтобы проверить что данный админ является главным
    main_admin_id = get_admin_cafe_id('YES')
    if message.from_user.id != main_admin_id:
        await message.answer('Вам <b>не доступен</b> данный функционал, потому что вы не являетесь '
                             'главным администратором.', parse_mode='html')
    else:
        await message.answer(f'Добро пожаловать <b>{message.from_user.username}</b> в меню управления админами',
                             reply_markup=action_with_adm(), parse_mode='html')
        # перевели в новый режим
        await AdminStatesGroup.control_admins.set()


async def edit_admins(message: types.Message) -> None:
    """Нажали на кнопу редактировать админов"""
    # смотрм сколько админов есть
    number_exist_admins = quantity_admins()
    if number_exist_admins == 1:
        await message.answer('В данный момент существует только 1 администратор (это Вы)')
        await message.answer('Пока что некого редактировать. Вернитесь позднее...')
    else:
        exist_admins = get_all_admins()
        await message.answer('Выберите админа, которому хотите выдать права...', reply_markup=show_admins(exist_admins))
        await AdminStatesGroup.choose_admin.set()


async def action_with_choose_admin(message: types.Message, state: FSMContext) -> None:
    """Проверяем что выбранный админ существует (корректные данные) и если всё ок предлагаем выдать ему нужные права"""
    # получили всех админов
    exist_admins = get_all_admins()
    # положили в ms
    async with state.proxy() as data:
        data['choose_admin'] = message.text

    check = data['choose_admin'].split()
    try:
        int(check[1])
    except ValueError:
        await message.answer('Такого админа не существует😔')
    except IndexError:
        await message.answer('Такого админа не существует😔')
    else:
        if tuple([int(check[1]), check[0]]) in exist_admins:
            await message.answer('Выберите какие права ему нужно выдать...', reply_markup=rights_for_admin())
            await AdminStatesGroup.get_rights.set()
        else:
            await message.answer('Такого админа не существует😔')


async def do_worker_cafe(message: types.Message, state: FSMContext) -> None:
    """Даём супер права работнику кафе"""

    # открываем ms и читаем id админа
    async with state.proxy() as data:
        id_need_admin = int(data['choose_admin'].split()[1])

    # выдаём нужные права на работу в кафе
    await create_cafe_worker(id_need_admin)

    await message.answer('Теперь данный админ помечен как работник кафе. (Ему и Вам будут приходить заказы)')


"""Создание событий в Тутаеве"""


async def adm_create_event(message: types.Message) -> None:
    """Только что пользователь нажал на кнопку создать мероприятие"""
    await message.answer(CREATE_NEW_ADV, reply_markup=exit_kb())
    await message.answer(EVENT_NAME)
    await AdminStatesGroup.e_name.set()


async def is_correct_name(message: types.Message) -> None:
    """Проверяем на корректность название события/бургера"""
    await message.answer(CORRECT_NAME)


async def get_name_of_event(message: types.Message, state: FSMContext) -> None:
    """Получаем название мероприятия и сохраняем в MemoryStorage"""
    async with state.proxy() as data:
        data['e_name'] = message.text
    await message.answer(NEED_DATE)
    await AdminStatesGroup.e_date.set()


async def is_correct_date(message: types.Message) -> None:
    """Проверяем на корректность даты"""
    await message.answer(CORRECT_DATE_ADV)


async def get_date_of_event(message: types.Message, state: FSMContext) -> None:
    """Получаем дату события и сохраняем в MemoryStorage"""
    async with state.proxy() as data:
        data['e_date'] = message.text
    await message.answer(GET_DESC_DATE_ADV)
    await AdminStatesGroup.e_descript.set()


async def is_correct_desc(message: types.Message) -> None:
    """Проверяем на корректность описание"""
    await message.answer('Должен быть текст')


async def get_descript_event(message: types.Message, state: FSMContext) -> None:
    """Получаем инф-цию об описании события"""
    async with state.proxy() as data:
        data['e_descript'] = message.text
    await message.answer(GET_PICT_ADV)
    await AdminStatesGroup.get_photo.set()


async def is_correct_photo(message: types.Message) -> None:
    """Проверяем на корректность фото"""
    await message.answer('Должно быть фото!')


async def get_photo_event(message: types.Message, state: FSMContext) -> None:
    """Получаем фото события"""
    async with state.proxy() as data:
        data['e_photo'] = message.photo[0].file_id
    await message.answer(NEED_LINK)
    await AdminStatesGroup.get_link.set()


async def dont_need_link(message: types.Message, state: FSMContext) -> None:
    """Не нужна ссылка переходим на показ составленной анкеты"""
    # сделали запись о ненадобности ссылки
    async with state.proxy() as data:
        data['link'] = '-'
    await message.answer(NO_LINK, reply_markup=get_do_post('👁 Показать анкету'))
    await AdminStatesGroup.ads_confirmation.set()


async def is_correct_link(message: types.Message) -> None:
    """Обработчик неправильной ссылки"""
    await message.answer('Ссылка не корректная!!!')


async def get_link_to_social_networks(message: types.Message, state: FSMContext) -> None:
    """Запрашиваем ссылку на событие (будем выдавать в виде inlint kb)"""

    # записали ссылку в MS
    async with state.proxy() as data:
        data['link'] = message.text
    await message.answer(LAST_STEP_ADV, reply_markup=get_do_post('👁 Показать анкету'))
    await AdminStatesGroup.ads_confirmation.set()


async def show_ads(message: types.Message, state: FSMContext) -> None:
    """Показываем анкету с только что введёнными данными"""
    async with state.proxy() as user_data:
        data = user_data
    # показываем без ссылки если её нет
    if data['link'] == '-':
        await bot.send_photo(chat_id=message.from_user.id, photo=data['e_photo'],
                             caption=f'<b>Название события:</b> {data["e_name"]}\n<b>Дата:</b> {data["e_date"]}\n'
                                     f'<b>Описание:</b> {data["e_descript"]}', parse_mode='html',
                             reply_markup=right_anket())
    else:
        await bot.send_photo(chat_id=message.from_user.id, photo=data['e_photo'],
                             caption=f'<b>Название события:</b> {data["e_name"]}\n<b>Дата:</b> {data["e_date"]}\n'
                                     f'<b>Описание:</b> {data["e_descript"]}', parse_mode='html',
                             reply_markup=link_in_button_adv(data['link']))
        await message.answer('Вам нравится анкета?', reply_markup=right_anket())


async def change_ads(message: types.Message) -> None:
    """Если пользователю что-то не понравилось в объявлении возвращаем его на этап создания"""
    await message.answer(WARNING_EDIT_A, reply_markup=ReplyKeyboardRemove())
    await message.answer('Введите название мероприятия:')
    await AdminStatesGroup.e_name.set()


async def add_ads_to_db(message: types.Message, state: FSMContext) -> None:
    """Если всё хорошо добавляем в бд"""
    # сходили в MemoryStorage и забрали данные
    async with state.proxy() as user_data:
        data = user_data
    # записали в бд
    await write_event_to_db(tuple([data['e_name'], data['e_photo'], data['e_descript'], data['e_date'], data['link']]))
    await message.answer(SUCESS_ADV_IN_DB, parse_mode='html', reply_markup=adm_opportunities())
    # перевели в главное меню админа
    await AdminStatesGroup.adm_control_panel.set()


"""Редактирование событий"""


async def list_events_to_edit(message: types.Message, state: FSMContext) -> None:
    """Редактирование уже созданных событий"""
    await message.answer(EDIT_EXIST_EVENTS)

    # нужен запрос к бд для проверки на существование событий
    # если их нет то отсылаем админа в гл меню
    db_records = await get_events_from_db()
    # записали сущ события в мs
    async with state.proxy() as data:
        data['events_exist_in_db'] = db_records

    if not db_records:
        await message.answer(NO_EVENTS_TO_EDIT)
    else:
        await message.answer(LIST_EXIST_EVENTS, reply_markup=view_events(db_records))
        await AdminStatesGroup.choose_edit_advs.set()


async def action_with_adv(message: types.Message, state: FSMContext) -> None:
    """Выбор действия Удаление поста/ изменение"""
    # записываем название и дату события которое будем удалять на след. шаге
    async with state.proxy() as data:
        # если нет такого события в кнопке -> сообщаем об ошибке и на гл.меню
        for_compare = message.text.split()
        try:
            int(for_compare[0])
        except ValueError:
            await message.answer(NO_EVENT, reply_markup=adm_opportunities())
            await AdminStatesGroup.adm_control_panel.set()
            return None
        if not any(map(lambda t: t[0] == int(for_compare[0]), data['events_exist_in_db'])):
            await message.answer(NO_EVENT, reply_markup=adm_opportunities())
            await AdminStatesGroup.adm_control_panel.set()
            return None
        data['delite_e'] = message.text.split()
    await message.answer('Отлично! Что будем делать?', reply_markup=del_or_edit())
    await AdminStatesGroup.edit_advs.set()


async def edit_exist_adv(message: types.Message, state: FSMContext) -> None:
    """Редактирование сущ.событий"""

    # удалили старое событие
    # заходим в MS и смотрим id/name/date мероприятия для удаления
    async with state.proxy() as data:
        need_d_for_del = data['delite_e']
    # удаление из бд
    await del_event_in_db(need_d_for_del)
    # и создаём новое
    await message.answer(WARNING_EDIT_A + '\nВведите название события: ', reply_markup=exit_kb())
    await AdminStatesGroup.e_name.set()


async def permanent_del(message: types.Message, state: FSMContext) -> None:
    """Действия для удаления поста"""

    # заходим в MS и смотрим id/name/date мероприятия для удаления
    async with state.proxy() as data:
        need_d_for_del = data['delite_e']
    # удаление из бд
    await del_event_in_db(need_d_for_del)

    await message.answer('Событие успешно удалено', reply_markup=adm_opportunities())
    await AdminStatesGroup.adm_control_panel.set()


"""Бургеры"""


async def burgers_menu(message: types.Message) -> None:
    """Отсюда идёт разветвление на Добавление/Редактирование"""
    await message.answer(BURGERS_MENU)
    await message.answer('Выберите что бы вы хотели сделать?', reply_markup=new_prod_or_edit_exist())
    await AdminStatesGroup.burgers_menu.set()


async def add_new_product(message: types.Message) -> None:
    """Добавление нового товара в меню бургеров"""
    await message.answer('Введите название нового товара:', reply_markup=exit_kb())
    await AdminStatesGroup.name_new_product.set()


async def get_name_burger(message: types.Message, state: FSMContext) -> None:
    """Получаем название товара и сохраняем в MemoryStorage"""
    async with state.proxy() as data:
        data['product_name'] = message.text
    await message.answer(GET_BURGER_PHOTO)
    await AdminStatesGroup.get_photo_dish.set()


async def get_burger_photo(message: types.Message, state: FSMContext) -> None:
    """Получаем фото товара"""
    async with state.proxy() as data:
        data['product_photo'] = message.photo[0].file_id
    await message.answer(DISH_DESCRIP)
    await AdminStatesGroup.dish_descript.set()


async def get_descript_dish(message: types.Message, state: FSMContext) -> None:
    """Получаем инф-цию об описании товара"""
    async with state.proxy() as data:
        data['product_descript'] = message.text
    await message.answer('Ослалось добавить последний пункт (цену за 1 шт)')
    await AdminStatesGroup.dish_price.set()


async def is_correct_price(message: types.Message) -> None:
    """В случае если некорректная цена"""
    await message.answer('Не верная цена! Цена должна быть текстом и содержать ТОЛЬКО цифры')


async def price(message: types.Message, state: FSMContext) -> None:
    """Цена за 1 товар"""
    # записали в MS
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отлично! Осталось всего лишь подтвердить правильность введённых данных',
                         reply_markup=get_do_post('👁 Показать фото-карточку товара'))
    await AdminStatesGroup.dish_confirmation.set()


async def show_dish(message: types.Message, state: FSMContext) -> None:
    """Показываем фото-карточку с только что введёнными данными"""
    async with state.proxy() as user_data:
        data = user_data
    # показываем
    await bot.send_photo(chat_id=message.from_user.id, photo=data['product_photo'],
                         caption=f'<b>Название:</b> {data["product_name"]}\n<b>Цена:</b> {data["price"]}\n'
                                 f'<b>Описание товара:</b> {data["product_descript"]}',
                         parse_mode='html', reply_markup=right_anket())


async def change_dish(message: types.Message) -> None:
    """Если пользователю что то не понравилось в объявлении возвращаем его на этап создания"""
    await message.answer(WARNING_EDIT_D)
    await message.answer('Введите название нового товара:', reply_markup=exit_kb())
    await AdminStatesGroup.name_new_product.set()


async def add_dish_to_db(message: types.Message, state: FSMContext) -> None:
    """Если всё хорошо добавляем товар в бд"""
    # сходили в MemoryStorage и забрали данные
    async with state.proxy() as user_data:
        data = user_data
    # записали в бд
    await create_menu(tuple(
        [data['product_photo'], data['product_name'], data['product_descript'], data['price']]))
    await message.answer('Отлично данные успешно записаны в бд!\nПеревожу в гл.меню', reply_markup=adm_opportunities())
    # перевели в главное меню админа
    await AdminStatesGroup.adm_control_panel.set()


"""Редактирование бургеров"""


async def list_dishes_to_edit(message: types.Message, state: FSMContext) -> None:
    """Редактирование уже созданных товаров"""
    await message.answer('В данном разделе можно редактировать меню с бургерами')

    # запрос к бд для проверки на существование товаров
    # если их нет то отсылаем админа в гл меню
    # записали сущ события в мs
    db_menu = await get_dishes_from_db()
    async with state.proxy() as data:
        data['menu_exist_in_db'] = db_menu

    if not db_menu:
        await message.answer('Пока что меню пусто :( Создайте фото-карточки товаров!')
    else:
        await message.answer('Вот меню в формате(id|товар|цена). Выберите нужное...',
                             reply_markup=view_events(db_menu))
        await AdminStatesGroup.choose_edit_dish.set()


async def action_with_dish(message: types.Message, state: FSMContext) -> None:
    """Выбор действия Удаление поста/ изменение"""
    # записываем id title price товара которое будем удалять на след. шаге
    async with state.proxy() as data:
        # если нет такого товара в кнопке -> сообщаем об ошибке и на гл.меню
        for_compare = message.text.split()
        try:
            int(for_compare[0])
        except ValueError:
            await message.answer(NO_DISH, reply_markup=adm_opportunities())
            await AdminStatesGroup.adm_control_panel.set()
            return None
        if not any(map(lambda t: t[0] == int(for_compare[0]), data['menu_exist_in_db'])):
            await message.answer(NO_DISH, reply_markup=adm_opportunities())
            await AdminStatesGroup.adm_control_panel.set()
            return None
        data['delite_d'] = message.text.split()
    await message.answer('Отлично! Что будем делать?', reply_markup=del_or_edit())
    await AdminStatesGroup.edit_dish.set()


async def edit_exist_dish(message: types.Message, state: FSMContext) -> None:
    """Редактирование сущ.товара"""

    # удалили старый
    # заходим в MS и смотрим id/title/price товара для удаления
    async with state.proxy() as data:
        need_d_for_del = data['delite_d']
    # удаление из бд
    await del_dish_in_db(need_d_for_del)
    # и создаём новое
    await message.answer('Сейчас будет предложено ввести новые данные приготовьтесь\nВведите название товара:',
                         reply_markup=exit_kb())
    await AdminStatesGroup.name_new_product.set()


async def permanent_del_dish(message: types.Message, state: FSMContext) -> None:
    """Действия для удаления товара"""

    # заходим в MS и смотрим id/name/date мероприятия для удаления
    async with state.proxy() as data:
        need_d_for_del = data['delite_d']
    # удаление из бд
    await del_dish_in_db(need_d_for_del)

    await message.answer('Товар успешно удалён из меню', reply_markup=adm_opportunities())
    await AdminStatesGroup.adm_control_panel.set()
