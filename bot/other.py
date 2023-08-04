# для всяких мелких побочных ф-ий
from datetime import datetime
import re


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
    if datetime.today().year <= u_date.year:
        ...
    elif datetime.today().month <= u_date.month:
        ...
    elif datetime.today().day <= u_date.day:
        ...
    elif u_date.year <= datetime.today().year + 3:
        ...
    else:
        flag = False
    return flag


def is_good_link(s: str) -> bool:
    """Ф-ия для проверки корректности введённой admin ссылки"""
    # Регулярное выражение для проверки ссылки
    url_pattern = re.compile(r'^https?://\S+$')
    return True if url_pattern.match(s) else False
