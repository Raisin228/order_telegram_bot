# для всяких мелких побочных ф-ий
from datetime import datetime


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
