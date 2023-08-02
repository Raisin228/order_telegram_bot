from aiogram.dispatcher.filters.state import StatesGroup, State


class UserMenuStatesGroup(StatesGroup):
    """Состояния, в которых может находиться пользователь"""
    viewing_menu = State()
