# сами обработчики администратора
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from order_telegram_bot.bot.config import *
from order_telegram_bot.bot.handlers.admin.admi_states import AdminStatesGroup
from order_telegram_bot.bot.keyboards.admin.replykb import *
from order_telegram_bot.bot.main import bot
from order_telegram_bot.sqlite_bot.sqlite import quantity_admins, create_admin, chose_admin_password, get_user_password
from order_telegram_bot.sqlite_bot.sqlite import write_event_to_db


async def cancel(message: types.Message, state: FSMContext) -> None:
    """Кнопка canel для выхода в самое главное меню"""
    await state.finish()
    await message.answer('Вы вышли в главное меню user', reply_markup=ReplyKeyboardRemove())


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
        await message.answer('Выберите что бы вы хотели сделать?', reply_markup=adm_opportunities())
        await AdminStatesGroup.adm_control_panel.set()
    else:
        await message.answer(UNCORECT_PASS, reply_markup=cancelkb())


async def adm_create_event(message: types.Message) -> None:
    """Только что пользователь нажал на кнопку создать мероприятие"""
    await message.answer(CREATE_NEW_ADV,
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('Введите название мероприятия:')
    await AdminStatesGroup.e_name.set()


async def is_correct_name(message: types.Message) -> None:
    """Проверяем на корректность название события"""
    await message.answer(CORRECT_NAME_ADV)


async def get_name_of_event(message: types.Message, state: FSMContext) -> None:
    """Получаем название мероприятия и сохраняем в MemoryStorage"""
    async with state.proxy() as data:
        data['e_name'] = message.text
    await message.answer('Теперь мне нужно записать дату начала события в формате чч.мм.гггг')
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
    await AdminStatesGroup.e_photo.set()


async def is_correct_photo(message: types.Message) -> None:
    """Проверяем на корректность фото"""
    await message.answer('Должно быть фото!')


async def get_photo_event(message: types.Message, state: FSMContext) -> None:
    """Получаем фото события"""
    async with state.proxy() as data:
        data['e_photo'] = message.photo[0].file_id
    await message.answer(LAST_STEP_ADV, reply_markup=adm_get_do_post())
    await AdminStatesGroup.ads_confirmation.set()


async def show_ads(message: types.Message, state: FSMContext) -> None:
    """Показываем анкету с только что введёнными данными"""
    async with state.proxy() as user_data:
        data = user_data
    await bot.send_photo(chat_id=message.from_user.id, photo=data['e_photo'],
                         caption=f'Название события - {data["e_name"]}\nДата: {data["e_date"]}\nОписание: '
                                 f'{data["e_descript"]}', reply_markup=right_anket())


async def change_ads(message: types.Message) -> None:
    """Если пользователю что то не понравилось в объявлении возвращаем его на этап создания"""
    await message.answer(
        'Предупреждение! Сейчас будет повторный процесс заполнения данных. '
        'Всё прошлые данные мероприятия будут утеряны. Сохраните их!', reply_markup=ReplyKeyboardRemove())
    await message.answer('Введите название мероприятия:')
    await AdminStatesGroup.e_name.set()


async def add_ads_to_db(message: types.Message, state: FSMContext) -> None:
    """Если всё хорошо добавляем в бд"""
    # сходили в MemoryStorage и забрали данные
    async with state.proxy() as user_data:
        data = user_data
    # записали в бд
    await write_event_to_db(tuple([data['e_name'], data['e_photo'], data['e_descript'], data['e_date']]))
    await message.answer('Отлично данные успешно записаны в бд!\nПеревожу в гл.меню', reply_markup=adm_opportunities())
    # перевели в главное меню админа
    await AdminStatesGroup.adm_control_panel.set()
