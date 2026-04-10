## Развёртка, управление проектом

### Клонирование репозитория
```
git clone git@github.com:2Grifon/dimatech_test_project.git
cd dimatech_test_project
```

### Запуск проекта
1. Убедиться что в проекте присутствует корректный **.env** файл с необходимыми настройками. В случае отсутствия создать на основе шаблона **default.env**
```
cp default.env .env
```
2. Перейти в каталог с [makefile](Makefile)
3. Использовать команду `make rebuild` для сборки проекта и запуска контейнеров
```
make rebuild
```
4. Испрользовать команду `make upgrade` для применения миграций и создания БД
```
make upgrade
```
5. Приложение будет доступно на http://localhost:8000/api, документация API: http://localhost:8000/docs


### Запуск без docker-compose
#### Требования
- Python 3.12+
- PostgreSQL 15+

1. Клонировать репозиторий
```
git clone git@github.com:2Grifon/dimatech_test_project.git
cd dimatech_test_project
```
2. Создать и активировать виртуальное окружение
```
python -m venv .venv
source .venv/bin/activate
```
3. Установить зависимости
```
pip install ./backend
```
4. Создать .env файл и задать параметры подключения к локальной БД
```
cp default.env .env
```
**Отредактировать .env:**

  - POSTGRES_HOST=localhost

  - POSTGRES_USER=postgres

  - POSTGRES_PASSWORD=<ваш пароль>

  - POSTGRES_DB=postgres

5. Применить миграции
```
make upgrade-local
```
6. Запустить сервер
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Настройки .env файла
- **Пример пустого .env файла**
 [default.env](default.env)

- **Fast API**
  - `SECRET_KEY` - Секрет для подписи JWT токенов
  - `PAYMENT_SECRET_KEY` - Секрет для проверки подписи вебхука

- **Postgres** - все настройки этого пункта будут использованы при первом создании БД, не рекомендуется изменять после создания базы
  - `POSTGRES_DB` - имя базы данных на сервере, в которой будут храниться все табилцы созданные по моделям джанго. Пример: `postgres`
  - `POSTGRES_USER` - имя пользователя с доступом к БД из пункта `POSTGRES_DB`. Пример: `postgres`
  - `POSTGRES_PASSWORD` - пароль от пользователя, можно использовать любой безопасный случайный пароль
  - `POSTGRES_HOST` - название сервера базы данных. По умолчанию должен быть: `postgres`

### Команды make
 - **build** - сборка образа проекта
 - **rebuild** - пересборка проекта
 - **up** - запуск проекта
 - **down** - остановка проекта
 - **reup** - перезапуск проекта
 - **alembic** - запускает alembic <args> внутри backend контейнера
 - **autogenerate m="msg"** - создаёт миграцию
 - **upgrade** - применяет миграции
 - **downgrade** - откат на одну миграцию

### Файловая структура
- **backend/** - основной сервис Python
  - **app/** - основное приложение
    - **core/** - конфигурация приложения, подключение к БД, базовые классы
    - **modules/** - все модули проекта
      - **users/** - пользователи и администраторы
      - **accounting/** - счета, платежи, вебхук
    - Файл [**main.py**](backend/app/main.py) - точка входа FastAPI
  - **alembic/** - конфигурация Alembic
    - **versions/** папка для хранения миграций
- **docker-compose.yml** - конфиг сервисов проекта
- **Makefile** - часто используемые команды для сборки, запуска и миграций
- **default.env** - пример переменных окружения


### Параметры тестовых пользователей
 - **User**:  user@example.com userpassword123
 - **Admin**: admin@example.com adminpassword123
