import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Список компаний, которые нас интересуют (можно задать ID)
EMPLOYER_IDS = [
    1455,  # HeadHunter
    1740,  # Яндекс
    3529,  # Сбер
    596610,  # АО СК СОГАЗ-Мед
    4649269,  # T1
    6528,  # Okkam
    5923,  # Ренессанс Банк
    625332,  # БУРГЕР КИНГ РОССИЯ
    78638,  # Т-Банк
    6189,  # Bell Integrator
    4716984,  # X5 Digital
]
