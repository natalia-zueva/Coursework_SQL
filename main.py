from config import config
from src.utils import get_companies, create_database, save_data_to_database
from src.DBManager import DBManager


def main():
    employer_ids = [
        "3127",  # Мегафон
        "3529",  # Сбер
        "78638",  # Тинькофф
        "1740",  # Яндекс
        "2748",  # Ростелеком
        "3776",  # МТС
        "2180",  # Ozon
        "1122462",  # Skyeng
        "15478",  # VK
        "84585",  # Авито
    ]
    params = config()
    database_name = 'hh'

    data = get_companies(employer_ids)
    create_database(database_name, params)
    save_data_to_database(data, database_name, params)

    db_manager = DBManager(database_name, params)

    print(db_manager.get_companies_and_vacancies_count())
    print(db_manager.get_all_vacancies())
    print(db_manager.get_avg_salary())
    print(db_manager.get_vacancies_with_higher_salary())

    keyword = input("Введите ключевое слово для поиска вакансий: ")
    vacancies = db_manager.get_vacancies_with_keyword(keyword)
    if vacancies:
        print(f"Вакансии, содержащие ключевое слово '{keyword}':")
        for vacancy in vacancies:
            print(vacancy)
    else:
        print(f"Вакансии с ключевым словом '{keyword}' не найдены.")


if __name__ == '__main__':
    main()
