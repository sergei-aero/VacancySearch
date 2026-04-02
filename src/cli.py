# src/cli.py
import sys
from src.db.manager import DBManager


def print_header(text: str):
    """Печатает заголовок раздела."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


def print_error(text: str):
    """Печатает сообщение об ошибке."""
    print(f"\n❌ Ошибка: {text}")


def print_success(text: str):
    """Печатает сообщение об успехе."""
    print(f"\n✅ {text}")


def print_info(text: str):
    """Печатает информационное сообщение."""
    print(f"\nℹ️ {text}")


def format_salary(salary_from, salary_to, currency):
    """Форматирует зарплату в читаемый вид."""
    if salary_from is None and salary_to is None:
        return "не указана"
    elif salary_from is not None and salary_to is not None:
        return f"{salary_from:,} - {salary_to:,} {currency}".replace(",", " ")
    elif salary_from is not None:
        return f"от {salary_from:,} {currency}".replace(",", " ")
    else:
        return f"до {salary_to:,} {currency}".replace(",", " ")


def show_companies_and_vacancies():
    """Выводит список компаний и количество вакансий."""
    result = DBManager.get_companies_and_vacancies_count()
    if not result:
        print_info("Нет данных о компаниях. Возможно, база пуста.")
        return
    print_header("Список компаний и количество вакансий")
    for idx, (name, count) in enumerate(result, start=1):
        print(f"{idx}. {name} — {count} вакансий")


def show_all_vacancies():
    """Выводит все вакансии с названием компании, зарплатой и ссылкой."""
    result = DBManager.get_all_vacancies()
    if not result:
        print_info("Нет вакансий в базе.")
        return
    print_header("Все вакансии")
    for idx, (company, title, salary_from, salary_to, currency, url) in enumerate(result, start=1):
        salary_str = format_salary(salary_from, salary_to, currency)
        print(f"{idx}. {title} в компании «{company}»")
        print(f"   Зарплата: {salary_str}")
        print(f"   Ссылка: {url}\n")


def show_avg_salary():
    """Выводит среднюю зарплату по всем вакансиям."""
    avg = DBManager.get_avg_salary()
    if avg is None:
        print_info("Невозможно вычислить среднюю зарплату: нет данных о зарплатах.")
    else:
        print_header("Средняя зарплата по вакансиям")
        print(f"Средняя зарплата: {avg:,.0f} руб.".replace(",", " "))


def show_vacancies_higher_salary():
    """Выводит вакансии с зарплатой выше средней."""
    result = DBManager.get_vacancies_with_higher_salary()
    if not result:
        print_info("Нет вакансий с зарплатой выше средней.")
        return
    print_header("Вакансии с зарплатой выше средней")
    for idx, (title, company, salary_from, salary_to, currency, url) in enumerate(result, start=1):
        salary_str = format_salary(salary_from, salary_to, currency)
        print(f"{idx}. {title} в компании «{company}»")
        print(f"   Зарплата: {salary_str}")
        print(f"   Ссылка: {url}\n")


def show_vacancies_by_keyword():
    """Поиск вакансий по ключевому слову в названии."""
    keyword = input("\nВведите ключевое слово для поиска: ").strip()
    if not keyword:
        print_error("Ключевое слово не может быть пустым.")
        return
    result = DBManager.get_vacancies_with_keyword(keyword)
    if not result:
        print_info(f"Вакансии, содержащие слово «{keyword}», не найдены.")
        return
    print_header(f"Вакансии по ключевому слову «{keyword}»")
    for idx, (title, company, salary_from, salary_to, currency, url) in enumerate(result, start=1):
        salary_str = format_salary(salary_from, salary_to, currency)
        print(f"{idx}. {title} в компании «{company}»")
        print(f"   Зарплата: {salary_str}")
        print(f"   Ссылка: {url}\n")


def run_cli():
    """Главное меню консольного интерфейса."""
    while True:
        print("\n" + "=" * 50)
        print("   УПРАВЛЕНИЕ ДАННЫМИ О ВАКАНСИЯХ (hh.ru)")
        print("=" * 50)
        print("1. Список компаний и количество их вакансий")
        print("2. Список всех вакансий")
        print("3. Средняя зарплата по вакансиям")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")
        print("-" * 50)

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_companies_and_vacancies()
        elif choice == "2":
            show_all_vacancies()
        elif choice == "3":
            show_avg_salary()
        elif choice == "4":
            show_vacancies_higher_salary()
        elif choice == "5":
            show_vacancies_by_keyword()
        elif choice == "0":
            print_success("До свидания!")
            sys.exit(0)
        else:
            print_error("Неверный ввод. Пожалуйста, выберите номер от 0 до 5.")
