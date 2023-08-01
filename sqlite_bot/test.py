import datetime

now = datetime.datetime.now()
date = '2023-07-30'

date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')

between = (now - date_obj).days
print(between)