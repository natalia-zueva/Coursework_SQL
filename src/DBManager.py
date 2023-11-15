import psycopg2


class DBManager:

    def __init__(self):
        pass

    def get_companies_and_vacancies_count(self, database_name, params):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        conn = psycopg2.connect(dbname=database_name, **params)

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
        pass

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        pass

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        pass

    def get_vacancies_with_keyword(self):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например, python.
        """
        pass
