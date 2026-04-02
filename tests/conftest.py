import pytest
from src.db.repository import get_connection, create_tables, insert_employers, insert_vacancies


@pytest.fixture
def sample_data():
    """Фикстура, которая заполняет БД тестовыми данными и очищает их после теста."""
    create_tables()

    # Очищаем таблицы перед тестом
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE vacancies, employers RESTART IDENTITY CASCADE;")

    # Вставляем тестовые данные
    employers = [
        {
            "id": 1,
            "name": "Test Company",
            "description": "Desc",
            "site_url": "https://test.com",
            "alternate_url": "https://test.com",
        }
    ]
    vacancies = [
        {
            "id": 101,
            "name": "Python Developer",
            "employer": {"id": 1},
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "alternate_url": "https://test.com/vac/101",
            "description": "Test",
            "published_at": "2023-01-01T00:00:00+0300",
        }
    ]
    insert_employers(employers)
    insert_vacancies(vacancies)

    yield  # здесь выполняется тест

    # После теста очищаем таблицы
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE vacancies, employers RESTART IDENTITY CASCADE;")
