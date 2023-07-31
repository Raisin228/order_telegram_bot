import sqlite3 as sq
import datetime


# создание базы данных
def db_start():
    global db, cursor

    db = sq.connect('test_base.db')
    cursor = db.cursor()

    # таблица для событий
    cursor.execute('CREATE TABLE IF NOT EXISTS events('
                   'num_id INTEGER PRIMARY KEY,'
                   ' photo TEXT,'
                   ' description TEXT,'
                   ' date TEXT)')

    # сохранение данных
    db.commit()


# шаблон для события
async def create_event():
    # получаем ключевое значение - порядковый номер
    try:
        event_last_id = int(cursor.execute('SELECT MAX(num_id) FROM events').fetchone()[0])
    except TypeError:
        event_last_id = 0

    event_new_id = event_last_id + 1
    # создаем новую строку с новым номером
    cursor.execute('INSERT INTO events VALUES(?, ?, ?, ?)', (event_new_id, '', '', ''))
    db.commit()


# заполнение данных о событии (Богдан делает)
async def edit_event(state):
    pass


# получение данных
def week_events():
    # список дат, входящих в текущую неделю
    ok_evens = list()
    # текущая дата
    now_date = datetime.datetime.now()
    # id всех событий
    events_id = cursor.execute('SELECT num_id FROM events').fetchall()

    # перебираем все события и ищем подходящие
    for event_id in events_id:
        data_event = cursor.execute('SELECT * FROM events WHERE num_id == {key}'.format(key=event_id[0])).fetchone()
        # объект с датой события
        date_obj = datetime.datetime.strptime(data_event[3], '%d.%m.%Y')
        # разница в днях
        count_days = (date_obj - now_date).days
        # подходящие берем
        if 0 <= count_days <= 7:
            ok_evens.append(data_event)
    return ok_evens




