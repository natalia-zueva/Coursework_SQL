# Задача проекта
В рамках проекта необходимо было получить данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.

### Основные шаги проекта
1. Получить данные о работодателях и их вакансиях с сайта hh.ru. Для этого используется публичный API hh.ru и библиотека requests.
2. Выбрать не менее 10 интересных вам компаний, от которых вы будете получать данные о вакансиях по API.
3. Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях. Для работы с БД используется библиотека psycopg2.
4. Реализовать код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
5. Создать класс DBManager для работы с данными в БД.

## Проект имеет следующую структуру:
Основной скрипт находится в файле main.py и готов к запуску. 

Что он делает:
- Импортирует конфигурацию, функции и методы класса DBManager из файлов config.py, utils.py и DBManager.py.
- Получает данные о компаниях с помощью функции get_companies.
- Создает базу данных и таблицы с помощью функции create_database.
- Сохраняет полученные данные в базу данных с помощью функции save_data_to_database.
- Создает экземпляр класса DBManager для работы с базой данных.
- Выводит информацию о компаниях и вакансиях с использованием методов класса DBManager.
- Позволяет пользователю ввести ключевое слово для поиска вакансий и выводит результаты поиска.

## Предварительные настройки
Файл зависимостей называется "pyproject.toml". В этом файле перечисляются все библиотеки и их версии, необходимые для работы проекта. Для установки зависимостей из "pyproject.toml", выполните:
poetry install


Для корректной работы БД и подключения необходимо создать и заполнить своими данными файл "database.ini":

[postgresql] #секция

host=localhost #ваш хост для подключения

user=postgres #ваше имя пользователя

password=password #ваш пароль

port=5432 #ваш порт

Т.к. это конфиденциальная информация не забудьте добавить файл в .gitignore.
