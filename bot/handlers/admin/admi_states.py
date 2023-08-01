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
