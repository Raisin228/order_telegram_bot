import datetime
import sqlite3 as sq


def db_start():
    """Создание базы данных"""

    global db, cursor

    db = sq.connect('test_base.db')
    cursor = db.cursor()

    # таблица для событий
    cursor.execute('CREATE TABLE IF NOT EXISTS events('
                   'id INTEGER PRIMARY KEY,'
                   ' photo TEXT,'
                   ' description TEXT,'
                   ' date TEXT)')

    # таблица с данными об администраторах
    cursor.execute('CREATE TABLE IF NOT EXISTS admins(admin_id INTEGER PRIMARY KEY, password TEXT, main TEXT)')

    # таблица для меню
    cursor.execute('CREATE TABLE IF NOT EXISTS menu('
                   'id INTEGER PRIMARY KEY,'
                   ' photo TEXT,'
                   ' title TEXT,'
                   ' description TEXT,'
                   ' price INTEGER)')

    # сохранение данных
    db.commit()


async def chose_admin_password() -> str:
    """Запрос на получение пароля 1 администратора"""
    return cursor.execute('SELECT * FROM admins WHERE main = "YES";').fetchone()[1]


def get_user_password(user_id: int) -> str:
    """Запрос на получение пароля от конкретного юзера"""
    param = cursor.execute(f'SELECT * FROM admins WHERE admin_id = {user_id}').fetchone()
    if param is not None:
        return param[1]


def quantity_admins() -> int:
    """Узнаём сколько администраторов в бд уже есть"""
    count = cursor.execute('SELECT COUNT(*) FROM admins;').fetchone()[0]
    return count


async def create_admin(user_id: int, password: str) -> str:
    """Создаём пустую ячейку в бд для конкретного админа"""
    param = quantity_admins()
    if cursor.execute(f'SELECT * FROM admins WHERE admin_id = {user_id}').fetchone() is None and param == 0:
        cursor.execute('INSERT INTO admins VALUES(?, ?, ?) ', (user_id, password, 'YES'))
        db.commit()
        return 'OK'
    elif cursor.execute(f'SELECT * FROM admins WHERE admin_id = {user_id}').fetchone() is None and param != 0:
        cursor.execute('INSERT INTO admins VALUES(?, ?, ?) ', (user_id, password, 'NO'))
        db.commit()
        return 'OK'


async def create_event():
    """ Шаблон для события """
    cursor.execute('INSERT INTO events(photo, description, date) VALUES(?, ?, ?)', ('', '', ''))
    db.commit()


async def create_menu():
    """Шаблон для элемента меню"""
    cursor.execute('INSERT INTO menu(photo, title, description, price) VALUES(?, ?, ?, ?)', ('', '', '', 0))
    db.commit()


def week_events():
    """Получение данных о событиях на 7 дней"""

    # список дат, входящих в текущую неделю
    ok_evens = list()
    # текущая дата
    now_date = datetime.datetime.now()
    # id всех событий
    events_id = cursor.execute('SELECT id FROM events').fetchall()

    # перебираем все события и ищем подходящие
    for event_id in events_id:
        data_event = cursor.execute('SELECT * FROM events WHERE id == {key}'.format(key=event_id[0])).fetchone()
        # объект с датой события
        date_obj = datetime.datetime.strptime(data_event[3], '%d.%m.%Y')
        # разница в днях
        count_days = (date_obj - now_date).days
        # подходящие берем
        if 0 <= count_days <= 7:
            ok_evens.append(data_event)
    return ok_evens


def menu_positions():
    """Получение списка позиций из меню"""

    # список названий всех продуктов
    menu_list = cursor.execute('SELECT * FROM menu').fetchall()
    # словарь с информацией о продуктах(ключ - название, значение список [фото, описание, цена])
    menu_dict = dict()
    # заполнение словаря
    for i in menu_list:
        menu_dict[i[2]] = [i[1], i[3], i[4]]
    return menu_dict
