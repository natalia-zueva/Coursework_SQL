import psycopg2
from config import config


class DBManager:

    def __init__(self, database_name, params=config()):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT employers.employer, COUNT(vacancies.vacancy_id) AS vacancy_count
                FROM employers
                LEFT JOIN vacancies ON employers.employer_id = vacancies.employer_id
                GROUP BY employers.employer
                """
            )

            data = cur.fetchall()

        conn.commit()
        conn.close()
        return data

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты, и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT employer, vacancy, salary_min, vacancy_url FROM vacancies
                """
            )

            data = cur.fetchall()

        conn.commit()
        conn.close()
        return data

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT round(AVG(salary_min)) as avg_salary FROM vacancies
                """
            )
            data = cur.fetchall()

        conn.commit()
        conn.close()
        return data

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_id, vacancy, salary_min FROM vacancies
                WHERE salary_min > (SELECT round(AVG(salary_min), 2) from vacancies)
                ORDER BY salary_min
                """
            )

            data = cur.fetchall()

        conn.commit()
        conn.close()
        return data

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например, python.
        """
        keyword1 = keyword.lower()
        keyword2 = keyword.title()
        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT vacancy_id, vacancy FROM vacancies
                WHERE vacancy LIKE '%{keyword1}%' OR vacancy LIKE '%{keyword2}%'
                """
            )

            data = cur.fetchall()

        conn.commit()
        conn.close()
        return data
