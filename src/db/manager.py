from src.db.repository import get_connection


class DBManager:
    """Класс для работы с данными в БД."""

    @staticmethod
    def get_companies_and_vacancies_count():
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        Возвращает список кортежей (company_name, vacancies_count).
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name, COUNT(v.id) as vacancies_count
                    FROM employers e
                    LEFT JOIN vacancies v ON e.id = v.employer_id
                    GROUP BY e.id, e.name
                    ORDER BY vacancies_count DESC;
                """)
                return cur.fetchall()

    @staticmethod
    def get_all_vacancies():
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        Возвращает список кортежей (company_name, vacancy_name, salary_from, salary_to, currency, url).
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id;
                """)
                return cur.fetchall()

    @staticmethod
    def get_avg_salary():
        """
        Получает среднюю зарплату по вакансиям.
        Для каждой вакансии зарплата вычисляется как:
        - (salary_from + salary_to)/2, если оба поля не NULL
        - salary_from, если salary_to NULL
        - salary_to, если salary_from NULL
        - NULL, если оба NULL
        Возвращает среднее арифметическое по всем вакансиям (float) или None.
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT AVG(
                        CASE
                            WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL THEN (salary_from + salary_to) / 2.0
                            WHEN salary_from IS NOT NULL THEN salary_from
                            WHEN salary_to IS NOT NULL THEN salary_to
                            ELSE NULL
                        END
                    ) as avg_salary
                    FROM vacancies
                    WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL;
                """)
                result = cur.fetchone()[0]
                return float(result) if result is not None else None

    @staticmethod
    def get_vacancies_with_higher_salary():
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        Возвращает список кортежей (vacancy_name, company_name, salary_from, salary_to, currency, url).
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    WITH vacancy_salary AS (
                        SELECT id,
                            CASE
                                WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL THEN (salary_from + salary_to) / 2.0
                                WHEN salary_from IS NOT NULL THEN salary_from
                                WHEN salary_to IS NOT NULL THEN salary_to
                                ELSE NULL
                            END AS calculated_salary
                        FROM vacancies
                    ),
                    avg_salary AS (
                        SELECT AVG(calculated_salary) AS avg_val
                        FROM vacancy_salary
                        WHERE calculated_salary IS NOT NULL
                    )
                    SELECT v.name, e.name, v.salary_from, v.salary_to, v.currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    JOIN vacancy_salary vs ON v.id = vs.id
                    CROSS JOIN avg_salary
                    WHERE vs.calculated_salary > avg_salary.avg_val
                    ORDER BY vs.calculated_salary DESC;
                """)
                return cur.fetchall()

    @staticmethod
    def get_vacancies_with_keyword(keyword: str):
        """
        Получает список всех вакансий, в названии которых содержится переданное слово (регистронезависимо).
        Возвращает список кортежей (vacancy_name, company_name, salary_from, salary_to, currency, url).
        """
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Используем ILIKE для регистронезависимого поиска
                cur.execute(
                    """
                    SELECT v.name, e.name, v.salary_from, v.salary_to, v.currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    WHERE v.name ILIKE %s;
                """,
                    (f"%{keyword}%",),
                )
                return cur.fetchall()
