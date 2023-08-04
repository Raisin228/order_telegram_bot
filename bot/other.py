# для всяких мелких побочных ф-ий
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
    # проверяем ещё и на emoji
    is_past = datetime.today().day <= u_date.day and \
              datetime.today().month <= u_date.month and datetime.today().year <= u_date.year
    if is_past and u_date.year <= datetime.today().year + 3:
        return True


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
