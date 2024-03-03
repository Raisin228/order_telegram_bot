# <a href='https://t.me/tutaev_events_bot'>КофеШтабот</a>

---

## Описание


**КофеШтабот** - это чат-бот, который создан по заказу кафе *"КофеШтаб"*.

* Если Вы когда-нибудь окажетесь в Тутаеве и в Вашей голове появится вопрос, *чем же мне заняться*? Какое мероприятие в
  городе посетить?

* Мы знаем ответ🔥🔥!! *Заходите в нашего бота*, он с радостью расскажет о ближайших событиях, которые будут
  происходить в Тутаеве. С помощью данного бота пользователь может узнать о ближайшем мероприятии в Тутаеве и посетить
  его.

* **Что за праздник без вкусной еды?** Подумала наша команда и добавила в функционал бота возможность заказывать🧢
  недорогие, качественные и очень вкусные бургеры из "КофеШтаб'а".

* Вам даже ~~не придётся думать~~ о том, как забрать
  заказ. Доверьте эту работу нашему боту. *Он мгновенно создаст заказ* и передаст его в работу сотрудникам
  заведения👩‍🍳👨‍🍳.
  Они максимально оперативно приготовят все заказанные товары, и вот уже сотрудник доставки будет мчаться🏃‍♂️ по
  указанному
  адресу, чтобы наши дорогие клиенты смогли отведать тёплых только что приготовленных бургеров🍔!

## Структура репозитория

---

- <a href='https://github.com/Raisin228/order_telegram_bot/tree/main/architectures'>**Architectures**</a> - папка с 
  архитектурой
- <a href='https://github.com/Raisin228/order_telegram_bot/tree/main/bot_scrins'>**Bot_scrins**</a> - папка со скринами работы бота
- <a href='https://github.com/Raisin228/order_telegram_bot/tree/main/bot'>**Bot**</a> - папка с основным кодом проекта
    - <a href='https://github.com/Raisin228/order_telegram_bot/tree/main/bot/handlers'>**Handlers**</a> - папка, в которой
      находятся обработчики на действия пользователей
        - <a href='https://github.com/Raisin228/order_telegram_bot/tree/main/bot/handlers/admin'>**Admin**</a> - папка с 
          файлами, отвечающими за функционал администратора
            - [*Admin_States.py*](https://github.com/Raisin228/order_telegram_bot/blob/main/bot/handlers/admin/admi_states.py) - состояния, в которых может находиться администратор
            - [*Ahendlers.py*](https://github.com/Raisin228/order_telegram_bot/blob/main/bot/handlers/admin/ahandlers.py') - обработчики взаимодействия с администраторами
        - <a href='https://github.com/Raisin228/order_telegram_bot/tree/main/bot/handlers/user'>**User**</a> - папка с 
          файлами, отвечающими за функционал пользователя
            - [*User_States.py*]('https://github.com/Raisin228/order_telegram_bot/blob/main/bot/handlers/user/user_states.py'>) - состояния для обычных пользователей
            - [*Uhandlers.py*]('https://github.com/Raisin228/order_telegram_bot/blob/main/bot/handlers/user/uhandlers.py'>) - обработчики взаимодействия с пользователями
    - <a href='https://github.com/Raisin228/order_telegram_bot/tree/main/bot/keyboards'>**Keyboards**</a> - папка со всеми 
      клавиатурами проекта
        - <a href='https://github.com/Raisin228/order_telegram_bot/tree/main/bot/keyboards/admin'>**Admin**</a> - 
          админские клавиатуры прописаны здесь
            - [*Inlinekb.py*]('https://github.com/Raisin228/order_telegram_bot/blob/main/bot/keyboards/admin/inlinekb.py'>) - inline клавиатуры
            - [*Replykb.py*]('https://github.com/Raisin228/order_telegram_bot/blob/main/bot/keyboards/admin/replykb.py'>) - reply клавиатуры
        - <a href='https://github.com/Raisin228/order_telegram_bot/tree/main/bot/keyboards/user'>**User**</a> - все 
          юзерские клавиатуры находятся в этой папке
            - [*Inlinekb.py*]('https://github.com/Raisin228/order_telegram_bot/blob/main/bot/keyboards/user/inlinekb.py'>) - inline клавиатуры
            - [*Replykb.py*]('https://github.com/Raisin228/order_telegram_bot/blob/main/bot/keyboards/user/replykb.py'>) - reply клавиатуры

    - <a href='https://github.com/Raisin228/order_telegram_bot/blob/main/bot/config.py'>*Config.py*</a> - тексты для бота
    - <a href='https://github.com/Raisin228/order_telegram_bot/blob/main/bot/main.py'>*Main.py*</a> - главная ф-ия, в 
      которой зарегистрированы все обработчики
    - <a href='https://github.com/Raisin228/order_telegram_bot/blob/main/bot/other.py'>*Other.py*</a> - всякие 
      вспомогательные ф-ии
    - <a href='https://github.com/Raisin228/order_telegram_bot/blob/main/bot/run.py'>*Run.py*</a> - запускать проект из 
      этого файла!
- <a href='https://github.com/Raisin228/order_telegram_bot/tree/main/sqlite_bot'>**Sqlite_Bot**</a> - папка для работы 
  с бд
    - <a href='https://github.com/Raisin228/order_telegram_bot/blob/main/sqlite_bot/sqlite.py'>*Sqlite.py*</a> - ф-ии 
      для взаимодействия с бд
- <a href='https://github.com/Raisin228/order_telegram_bot/blob/main/.gitignore'>*.gitignore*</a> - .gitignore
- <a href='https://github.com/Raisin228/order_telegram_bot/blob/main/Procfile'>*Procfile*</a> - здесь написано, какой 
файлик должен запускаться интерпретатором, для деплоя на сервере (Railway)
- <a href='https://github.com/Raisin228/order_telegram_bot/blob/main/requirements.txt'>*Requirements.txt*</a> - 
библиотеки и зависимости

## Краткое описание основного функционала

*Производится с админ панели:*
  * Создание событий в Тутаеве
  * Изменение существующих событий (удаление/изменение)
  * Составление меню ресторана
  * Изменение товаров (удаление/изменение)
  * Генерация пароля - выдача прав пользователю на работника кафе (скрытая команда /adm_actions) 

*Действия доступные обычному пользователю:*
  * Просмотр ближайших event'ов в Тутаеве
  * Покупка товаров в ресторане (добавление в корзину/очистка корзины/оплата)
  * Возможность стать администратором (скрытая команда /hide)
  * Возможность стать работником кафе (скрытая команда /get_rights)

## Запуск бота

---

* Клонируйте репозиторий себе на локальную машину `git clone ссылка на репозиторий`
* Создайте виртуальное окружение `python -m venv venv`
* Активируйте окружение `venv/Scripts/activate`
* Установите все зависимости из requirements.txt `pip install -r requirements.txt`
* Зайдите в [BotFather](https://t.me/BotFather) и создайте нового бота (получите API ключ)
* Получите токен для геолокации в Яндекс
* В директории order_telegram_bot создайте файлик *.env* и вставьте в него следующее  
  `API_KEY='Ваш токен бота'`  
  `YANDEX_GEO_TOKEN='Ваш токен для геолокации'`  
  `PAY_TOKEN='Платёжный токен'`
* Запустите run.py
* Наслаждайтесь работой бота🔥🔥

## Стек технологий

---

1. [Python3](https://www.python.org/) - язык программирования
2. [Aiogram](https://docs.aiogram.dev/en/dev-3.x/) - асинхронная библиотека для написания тг ботов
3. [SQLite](https://www.sqlite.org/index.html) - реляционная база данных для хранения информации о пользователях

## Команда

---

- [Сальников Кирилл](https://vk.com/k.salnikov2020) - разработчик
- [Атрошенко Богдан](https://vk.com/bog_at_04) - разработчик

## Архитектура

---

### Логика работы администратор
<img src="https://github.com/Raisin228/order_telegram_bot/blob/main/architectures/%D0%B0%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%B0_%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD.png">

### Логика работы пользователь
<img src="https://github.com/Raisin228/order_telegram_bot/blob/main/architectures/user_arhit.jpg">


## Фото проекта

---

### Начало работы
<img src="https://github.com/Raisin228/order_telegram_bot/blob/main/bot_scrins/start_work.png">

### Просмотр ближайших событий
<img src="https://github.com/Raisin228/order_telegram_bot/blob/main/bot_scrins/viewing_events.png">

### Добавление бургера в коризну
<img src="https://github.com/Raisin228/order_telegram_bot/blob/main/bot_scrins/ordering_goods.png">

### Оплата по карте
<img src="https://github.com/Raisin228/order_telegram_bot/blob/main/bot_scrins/pay_bill.png">

### Админская клавиатура
<img src="https://github.com/Raisin228/order_telegram_bot/blob/main/bot_scrins/adm_actions.png">

### Генерировать ключ для расширения прав пользователя
<img src="https://github.com/Raisin228/order_telegram_bot/blob/main/bot_scrins/generate_key.png">
