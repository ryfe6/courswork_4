import json
import logging
from typing import Any

from src.classes import HeadHunterAPI, SuperJobAPI, Vacancy, WriteInfo


def get_vacancy(script: str, profession: str) -> None:
    """
    Функция С помощью полученных данных запускает один из трех сценариев.
    :param script: Номер сценария
    :param profession: Имя профессии
    :return: None
    """
    if script == "1":  # Сценарий 1) Парсинг данных с сайта hh.ru
        hh_api = HeadHunterAPI()
        hh_api.get_vacancies(profession)
    elif script == "2":  # Сценарий 2) Парсинг данных с сайта SuperJob
        sj_api = SuperJobAPI()
        sj_api.get_vacancies(profession)

    elif script == "3":  # Сценарий 3) Парсинг данных с сайтов hh.ru и SuperJob
        hh_api = HeadHunterAPI()
        sj_api = SuperJobAPI()
        hh_api.get_vacancies(profession)
        sj_api.get_vacancies(profession)


def filter_vacancy_and_write(profession: str, list_params: list ) -> None:
    """
    Функция для фильтрации вакансий и записи их в файл.
    :param profession: Имя профессии.
    :param list_params: Список параметров для фильтрации.
    """
    vac = Vacancy(list_params[0], list_params[1], list_params[2], list_params[3], list_params[4])
    vac.sorted_vacancies()
    WriteInfo().data_write(profession)


def parameters(name: str, url: str, pay_to: str, pay_from: str, requirement: str) -> list:
    """
    Функция принимает параметры от пользователя, обрабатывает их и убирает в список.
    :param name: Текст, который должен находиться в имени вакансии.
    :param url: Ссылка на вакансию.
    :param pay_to: Максимальная заработная плата.
    :param pay_from: Минимальная заработная плата.
    :param requirement: Тест, который должен находиться в описании вакансии.
    :return: Возвращает список с обработанными параметрами.
    """
    param_d = [name, url, pay_to, pay_from, requirement]
    new_params = []
    for param in param_d:
        if param == "":
            param = None
        try:
            param = int(param)
        except Exception as e:
            logging.error(e)
        new_params.append(param)
    return new_params


def bf_write(filename: str) -> None:
    with open(f"../data/{filename}.json", "r", encoding="utf8") as file:
        json_file = json.load(file)
        for line in json_file:
            print(
                f"""Заказчик: {line['employer']}
            Имя профеcсии: {line['name']}
            Ссылка на профессию: {line['url']}
            Описание вакансии: {line['requirement']}
            Зарплата от: {line['salary_from']}
            Зарплата до: {line['salary_to']}"""
            )


def sort_vacancy(filename: str) -> None:
    """"""
    with open(f"../data/{filename}.json", "r", encoding="utf-8") as file:
        json_file = json.load(file)
        sort = sorted(json_file, key=lambda x: x["salary_to"], reverse=True)

    with open(f"../data/{filename}.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(sort, indent=2, ensure_ascii=False))


def start() -> Any:
    """Функция в которую заложен сценарий выполнения программы."""
    print(
        """Приветствую тебя пользователь!!!
             Тебе нужна работа?
             Введи 1 - Да, нуждаюсь в работе...
             Введи 2 - Не, блатные не работают..."""
    )
    user_input = input()
    if user_input == "1":
        pass
    else:
        return "Хорошо, если понадобится работа, вы знаете какое приложение вам поможет..."

    print("""Введите имя профессии, чтобы подобрать нужные вакансии""")
    user_input_profession = input()
    print(
        """Отлично, в два клика мы сможем подобрать для тебя подходящие вакансии
         Введи 1 - Подберем для тебя вакансии с сайта hh.ru
         Введи 2 - Подберем для тебя вакансии с сайта SuperJob
         Введи 3 - Подберем для тебя вакансии с сайта hh.ru и SuperJob"""
    )
    user_input = input()
    if user_input == "1":
        get_vacancy("1", user_input_profession)
    elif user_input == "2":
        get_vacancy("2", user_input_profession)
    elif user_input == "3":
        get_vacancy("3", user_input_profession)
    else:
        return "Жаль, что мы не смогли вам помочь найти работу :("
    print(
        """Хотите настроить фильтр?
             Введите y/n"""
    )
    user_input = input().lower()
    if user_input == "y":
        print("""Если не хотите заполнять параметр, ничего не надо вводить""")
        user_input_name = input("Введите имя профессии - ")
        user_input_url = input("Введите ссылку на нужную профессию -")
        user_input_pay_to = input("Введите максимальную сумму заработной платы - ")
        user_input_pay_from = input("Введите минимальную сумму заработной платы - ")
        user_input_requirement = input("Введите слова, которые должны присутствовать в описании вакансии - ")
        params = parameters(
            name=user_input_name,
            url=user_input_url,
            pay_to=user_input_pay_to,
            pay_from=user_input_pay_from,
            requirement=user_input_requirement,
        )
        filter_vacancy_and_write(user_input_profession, params)
    else:
        print("Оставляем стандартные параметры")
        params = [None, None, None, None, None]
        filter_vacancy_and_write(user_input_profession, params)
        bf_write(user_input_profession)
    print(f"Данные сохранены в файл ../data/{user_input_profession}.json")
    print(
        """Отсортировать данные по убыванию заработной платы?
             Введите y/n"""
    )
    user_input = input()
    if user_input == "y":
        sort_vacancy(user_input_profession)
        bf_write(user_input_profession)
    else:
        pass
    print(
        """Хотите вывести в файл топ 5 самых высокооплачиваемых вакансий
    Введи y/n"""
    )
    user_input = input()
    if user_input == "y":
        sort_vacancy(user_input_profession)
        with open(f"../data/{user_input_profession}.json", "r", encoding="utf8") as file:
            json_file = json.load(file)
            top_vacancy = json_file[0:5]
        with open(f"../data/top_{user_input_profession}.json", "w", encoding="utf8") as file:
            file.write(json.dumps(top_vacancy, indent=2, ensure_ascii=False))
        print(f"""Данные выведены в файл ../data/top_{user_input_profession}.json""")
    else:
        pass
    print("Спасибо, что пользуетесь нашим приложением :)")
