import psycopg2
from psycopg2.extras import execute_values
from contextlib import contextmanager
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
import logging

logger = logging.getLogger(__name__)


@contextmanager
def get_connection():
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_tables():
    """Создаёт таблицы, если их нет."""
    from src.db.models import CREATE_EMPLOYERS_TABLE, CREATE_VACANCIES_TABLE

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_EMPLOYERS_TABLE)
            cur.execute(CREATE_VACANCIES_TABLE)
            logger.info("Таблицы созданы или уже существуют.")


def insert_employers(employers_data):
    """Вставляет список работодателей. Если конфликт по id — обновляет."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            query = """
            INSERT INTO employers (id, name, description, site_url, alternate_url)
            VALUES %s
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                site_url = EXCLUDED.site_url,
                alternate_url = EXCLUDED.alternate_url;
            """
            # Преобразуем данные в список кортежей
            data = [
                (e["id"], e["name"], e.get("description"), e.get("site_url"), e["alternate_url"])
                for e in employers_data
            ]
            execute_values(cur, query, data)
            logger.info(f"Загружено/обновлено {len(data)} работодателей.")


def insert_vacancies(vacancies_data):
    """Вставляет список вакансий. При конфликте id игнорируем (или можно обновлять)."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            query = """
            INSERT INTO vacancies (
                id, name, employer_id, salary_from, salary_to, currency, url, description, published_at
            ) VALUES %s
            ON CONFLICT (id) DO NOTHING;
            """
            data = []
            for v in vacancies_data:
                salary = v.get("salary")
                salary_from = salary["from"] if salary and salary.get("from") else None
                salary_to = salary["to"] if salary and salary.get("to") else None
                currency = salary["currency"] if salary and salary.get("currency") else None
                published_at = v.get("published_at")  # строка, можно преобразовать в timestamp позже

                data.append(
                    (
                        v["id"],
                        v["name"],
                        v["employer"]["id"],
                        salary_from,
                        salary_to,
                        currency,
                        v["alternate_url"],
                        v.get("description"),
                        published_at,
                    )
                )
            execute_values(cur, query, data)
            logger.info(f"Загружено {len(data)} вакансий.")
