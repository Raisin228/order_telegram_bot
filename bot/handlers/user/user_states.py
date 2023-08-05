from aiogram.dispatcher.filters.state import StatesGroup, State


class UserMenuStatesGroup(StatesGroup):
    """Состояния, в которых может находиться пользователь"""

    # состояние для просмотра меню
    viewing_menu = State()

    # состояние для оформления заказа
    enter_address = State()
    choice_payment = State()
