from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStatesGroup(StatesGroup):
    """Состояния в которых может находиться admin"""
    hide_field = State()
    enter_login = State()
    enter_password = State()
