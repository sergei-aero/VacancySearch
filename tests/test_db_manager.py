import pytest
from src.db.manager import DBManager
from src.db.repository import get_connection, create_tables, insert_employers, insert_vacancies


@pytest.fixture
def sample_data():
    create_tables()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE vacancies, employers RESTART IDENTITY CASCADE;")

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
    yield
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE vacancies, employers RESTART IDENTITY CASCADE;")


def test_get_companies_and_vacancies_count(sample_data):
    result = DBManager.get_companies_and_vacancies_count()
    assert len(result) == 1
    assert result[0][0] == "Test Company"
    assert result[0][1] == 1


def test_get_all_vacancies(sample_data):
    result = DBManager.get_all_vacancies()
    assert len(result) == 1
    assert result[0][1] == "Python Developer"


def test_get_avg_salary(sample_data):
    avg = DBManager.get_avg_salary()
    assert avg == 125000.0


def test_get_vacancies_with_higher_salary(sample_data):
    vacancies_low = [
        {
            "id": 102,
            "name": "Junior",
            "employer": {"id": 1},
            "salary": {"from": 50000, "to": 70000, "currency": "RUR"},
            "alternate_url": "https://test.com/vac/102",
            "description": "Test",
            "published_at": "2023-01-01T00:00:00+0300",
        }
    ]
    insert_vacancies(vacancies_low)
    result = DBManager.get_vacancies_with_higher_salary()
    assert len(result) == 1
    assert result[0][0] == "Python Developer"


def test_get_vacancies_with_keyword(sample_data):
    result = DBManager.get_vacancies_with_keyword("python")
    assert len(result) == 1
    result2 = DBManager.get_vacancies_with_keyword("java")
    assert len(result2) == 0
