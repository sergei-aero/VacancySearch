## VacancySearch

Приложение для загрузки данных о компаниях и вакансиях с сайта hh.ru в PostgreSQL, с возможностью последующего анализа через класс `DBManager`.

## Особенности

- Получение данных о работодателях и вакансиях через публичный API hh.ru.
- Проектирование и создание таблиц в PostgreSQL.
- Загрузка данных в базу с использованием `psycopg2`.
- Класс `DBManager` для выполнения аналитических запросов:
  - Список компаний и количество вакансий.
  - Все вакансии с деталями.
  - Средняя зарплата по вакансиям.
  - Вакансии с зарплатой выше средней.
  - Поиск вакансий по ключевому слову в названии.

## Технологии

- Python 3.9+
- PostgreSQL 16+
- requests
- psycopg2-binary
- python-dotenv
- flake8, black, isort, mypy (линтеры и форматтеры)

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/sergei-aero/VacancySearch.git
   cd VacancySearch
   
2. Создайте и активируйте виртуальное окружение:
   '''bash
    python -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate      # Windows
3. Установите зависимости:
   '''bash
   pip install -r requirements.txt
4. Настройте подключение к PostgreSQL:

- Создайте базу данных hh_vacancies.

- Скопируйте .env.example в .env и укажите параметры подключения:

text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hh_vacancies
DB_USER=postgres
DB_PASSWORD=ваш_пароль
5. Запустите приложение:

bash
python src/main.py

