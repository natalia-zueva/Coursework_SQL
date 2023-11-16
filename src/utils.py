import requests
import psycopg2


def get_companies(employer_ids: list[str]):
    """ Получение данных о компаниях"""
    data = []
    for employer_id in employer_ids:
        url = f'https://api.hh.ru/employers/{employer_id}'
        employer_response = requests.get(url)
        employer_data = employer_response.json()
        vacancy_response = requests.get(employer_data["vacancies_url"])
        vacancy_data = vacancy_response.json()
        data.append({
            'employer': employer_data,
            'vacancies': vacancy_data['items']
        })

    return data


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                employer VARCHAR(100) NOT NULL,
                open_vacancies INTEGER,
                vacancies_url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                employer VARCHAR(100) NOT NULL,
                vacancy VARCHAR(255) NOT NULL,
                salary_min INTEGER,
                vacancy_url TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict], database_name: str, params: dict):
    """Сохранение данных о компаниях и вакансиях в базу данных"""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in data:
            cur.execute(
                """
                INSERT INTO employers (employer_id, employer, open_vacancies, vacancies_url)
                VALUES (%s, %s, %s, %s)
                RETURNING employer_id
                """,
                (company['employer']['id'],
                 company['employer']['name'],
                 company['employer']['open_vacancies'],
                 company['employer']['vacancies_url'])
            )
            employer_id = cur.fetchone()
            for vacancy in company['vacancies']:
                if vacancy['salary'] is not None:
                    vacancy['salary'] = 0 if vacancy['salary']['from'] is None else vacancy[
                        'salary']['from']
                else:
                    vacancy['salary'] = 0
                cur.execute(
                        """
                        INSERT INTO vacancies (employer_id, employer, vacancy, salary_min,vacancy_url)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (employer_id,
                         vacancy['employer']['name'],
                         vacancy['name'],
                         vacancy['salary'],
                         vacancy['alternate_url'])
                    )

    conn.commit()
    conn.close()
