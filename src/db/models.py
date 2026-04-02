CREATE_EMPLOYERS_TABLE = """
CREATE TABLE IF NOT EXISTS employers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    site_url VARCHAR(255),
    alternate_url VARCHAR(255)
);
"""

CREATE_VACANCIES_TABLE = """
CREATE TABLE IF NOT EXISTS vacancies (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    employer_id INTEGER NOT NULL REFERENCES employers(id) ON DELETE CASCADE,
    salary_from INTEGER,
    salary_to INTEGER,
    currency VARCHAR(10),
    url VARCHAR(255),
    description TEXT,
    published_at TIMESTAMP,
    CONSTRAINT fk_employer FOREIGN KEY (employer_id) REFERENCES employers (id)
);
"""
