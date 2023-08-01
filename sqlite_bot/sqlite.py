import sqlite3 as sq
import datetime


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

    # таблица для меню
    cursor.execute('CREATE TABLE IF NOT EXISTS menu('
                   'id INTEGER PRIMARY KEY,'
                   ' photo TEXT,'
                   ' title TEXT,'
                   ' description TEXT,'
                   ' price INTEGER)')

    # сохранение данных
    db.commit()


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
