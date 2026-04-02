import requests
import time
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class HHClient:
    BASE_URL = "https://api.hh.ru/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "VacancySearch/1.0 (pavlov.aero@gmail.com)"})

    def get_employer(self, employer_id: int) -> Dict[str, Any]:
        """Получить данные о работодателе по ID."""
        url = f"{self.BASE_URL}employers/{employer_id}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе работодателя {employer_id}: {e}")
            return {}

    def get_vacancies(self, employer_id: int, per_page: int = 100) -> List[Dict[str, Any]]:
        """Получить все вакансии работодателя (с учётом пагинации)."""
        vacancies = []
        page = 0
        while True:
            try:
                url = f"{self.BASE_URL}vacancies"
                params = {"employer_id": employer_id, "per_page": per_page, "page": page}
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                items = data.get("items", [])
                vacancies.extend(items)

                # Если страниц больше нет, выходим
                page_count = data.get("pages", 0)
                if page >= page_count - 1:
                    break
                page += 1

                # Задержка, чтобы не нагружать API (рекомендации hh.ru)
                time.sleep(0.5)
            except requests.RequestException as e:
                logger.error(f"Ошибка при запросе вакансий для работодателя {employer_id}, страница {page}: {e}")
                break
        return vacancies
