from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStatesGroup(StatesGroup):
    """Состояния в которых может находиться admin"""
    # скрытое поле
    hide_field = State()

    # ввод нового пароля
    enter_new_password = State()

    # подтверждение пароля 1 админа
    enter_pass_conf = State()

    # ввод пароля при входе
    enter_password = State()

    # состояние панель админа
    adm_control_panel = State()

    # бот находиться в состоянии получения названия мероприятия
    e_name = State()

    # дата
    e_date = State()

    # ожидаем описание мероприятия
    e_descript = State()

    # получаем фото события
    e_photo = State()

    # получаем ссылку
    get_link = State()

    # подтверждение созданного события
    ads_confirmation = State()

    # редактирование событий
    edit_advs = State()

    # выбор нужного события
    choose_edit_advs = State()

