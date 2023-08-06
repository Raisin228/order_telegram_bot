# для всяких мелких побочных ф-ий
import re
from datetime import datetime

import requests


def my_pred(s: str) -> bool:
    """Проверка корректности даты события"""
    try:
        n_s = s.split('.')
        # потому что год мес день
        u_date = datetime(int(n_s[2]), int(n_s[1]), int(n_s[0]))
    except Exception:
        return False

    flag = True
    # проверка что дата актуальная
    if datetime.today().year <= u_date.year <= datetime.today().year + 3:
        ...
    elif datetime.today().month <= u_date.month:
        ...
    elif datetime.today().day <= u_date.day:
        ...
    else:
        flag = False
    return flag


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
