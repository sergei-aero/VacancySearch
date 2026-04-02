import logging
from src.api.hh_client import HHClient
from src.config import EMPLOYER_IDS
from src.db.repository import create_tables, insert_employers, insert_vacancies
from src.cli import run_cli

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # 1. Создаём таблицы
    create_tables()

    # 2. Инициализируем клиента API
    client = HHClient()

    # 3. Собираем данные по работодателям
    employers_data = []
    all_vacancies = []
    for emp_id in EMPLOYER_IDS:
        logger.info(f"Обработка работодателя {emp_id}")
        employer = client.get_employer(emp_id)
        if employer:
            employers_data.append(employer)
            vacancies = client.get_vacancies(emp_id)
            all_vacancies.extend(vacancies)
        else:
            logger.warning(f"Не удалось получить данные по работодателю {emp_id}")

    # 4. Загружаем работодателей в БД
    if employers_data:
        insert_employers(employers_data)

    # 5. Загружаем вакансии
    if all_vacancies:
        insert_vacancies(all_vacancies)

    logger.info("Загрузка данных завершена.")

    # 6. Запускаем пользовательский интерфейс для аналитики
    print("\nДанные успешно загружены в базу.")
    run_cli()

if __name__ == "__main__":
    main()

