# для всяких мелких побочных ф-ий
import re
import secrets
from datetime import datetime, timedelta

import requests

from order_telegram_bot.sqlite_bot.sqlite import get_right_pass


def my_pred(s: str) -> bool:
    """Проверка корректности даты события"""
    try:
        # Преобразуем введенную строку в объект datetime
        n_s = s.split('.')
        # потому что год мес день
        u_date = datetime(int(n_s[2]), int(n_s[1]), int(n_s[0]))

        # Получаем текущую дату
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Проверяем, что введенная дата не в прошлом и не дальше чем через 3 года
        if today <= u_date <= today + timedelta(days=3 * 365):
            return True
        else:
            return False
    except Exception:
        return False


def is_good_link(s: str) -> bool:
    """Ф-ия для проверки корректности введённой admin ссылки"""
    # Регулярное выражение для проверки ссылки
    url_pattern = re.compile(r'^https?://\S+$')
    return True if url_pattern.match(s) else False


def check_address(address, token):
    """Функция для проверки адреса через Yandex API Geocoder"""
    params = {
        "apikey": token,
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": address
    }
    response = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=params)
    data = response.json()
    ch = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
        'GeocoderMetaData']['kind']
    if ch == 'house':
        return 0
    else:
        return -1


def phone_check(num):
    """Проверка корректности номера телефона"""
    check = re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', num)
    if check:
        return True
    else:
        return False


def generate_pass() -> str:
    """Генерация пароля длины 8 символов"""
    password = secrets.token_hex(4)
    return password


def is_valid_password(password: str) -> bool:
    """Является ли данный пароль корректным и актуальным для выдачи прав"""

    # делаем запрос в бд и забираем оттуда пароль
    clue_date_from_db = get_right_pass()
    # проверяем что пароль совпадает и он валидный по дате
    if password == clue_date_from_db[0] and \
            datetime.now() - datetime.strptime(clue_date_from_db[1], "%d.%m.%Y") <= timedelta(days=1):
        return True
    return False

