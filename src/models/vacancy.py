from dataclasses import dataclass
from typing import Optional


@dataclass
class Employer:
    id: int
    name: str
    description: Optional[str]
    site_url: Optional[str]
    alternate_url: str
    # другие поля по необходимости


@dataclass
class Vacancy:
    id: int
    name: str
    employer_id: int
    salary_from: Optional[int]
    salary_to: Optional[int]
    currency: Optional[str]
    url: str
    description: Optional[str]  # можно достать из поля description
    published_at: str
