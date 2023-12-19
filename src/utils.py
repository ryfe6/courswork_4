import sys
from typing import Any

from src.classes import HeadHunterAPI, SuperJobAPI, Vacancy, WorkVacancy, WriteInfo


def script_vacancy(script: str, profession: str) -> None:
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
    else:
        sys.exit("Жаль, что мы не смогли вам помочь найти работу :(")


def start() -> Any:
    """Функция в которую заложен сценарий выполнения программы."""
    print(
        "Приветствую тебя пользователь!!!\n"
        "Тебе нужна работа?\n"
        "Введи 1 - Да, нуждаюсь в работе...\n"
        "Введи 2 - Не, блатные не работают..."
    )
    user_input = input()
    if user_input == "1":
        pass
    else:
        sys.exit("Хорошо, если понадобится работа, вы знаете какое приложение вам поможет...")

    print("Введите имя профессии, чтобы подобрать нужные вакансии")
    user_input_profession = input()
    print(
        "Отлично, в два клика мы сможем подобрать для тебя подходящие вакансии\n"
        "Введи 1 - Подберем для тебя вакансии с сайта hh.ru\n"
        "Введи 2 - Подберем для тебя вакансии с сайта SuperJob\n"
        "Введи 3 - Подберем для тебя вакансии с сайта hh.ru и SuperJob"
    )
    user_input = input()
    script_vacancy(user_input, user_input_profession)
    print("Хотите настроить фильтр?\n" "Введите y/n")
    user_input = input().lower()
    if user_input == "y":
        print("""Если не хотите заполнять параметр, ничего не надо вводить""")
        user_input_name = input("Введите имя профессии - ")
        user_input_url = input("Введите ссылку на нужную профессию -")
        user_input_pay_to = input("Введите максимальную сумму заработной платы - ")
        user_input_pay_from = input("Введите минимальную сумму заработной платы - ")
        user_input_requirement = input("Введите слова, которые должны присутствовать в описании вакансии - ")
        Vacancy(
            name=user_input_name,
            url=user_input_url,
            pay_to=user_input_pay_to,
            pay_from=user_input_pay_from,
            requirement=user_input_requirement,
        ).filter_vacancies()
    else:
        print("Оставляем стандартные параметры")
        Vacancy().filter_vacancies()
    WriteInfo(user_input_profession).data_write()
    WorkVacancy(user_input_profession).bf_print()
    print(f"Данные сохранены в файл ../data/{user_input_profession}.json")
    print("Отсортировать данные по убыванию заработной платы?\n" "Введите y/n")
    user_input_sort = input()
    if user_input_sort == "y":
        work_vacancy = WorkVacancy(user_input_profession)
        work_vacancy.sort_vacancy()
        work_vacancy.bf_print()
    else:
        pass
    print("Хотите вывести в файл топ 5 самых высокооплачиваемых вакансий\n" "Введи y/n")
    user_input = input()
    if user_input == "y":
        if user_input_sort != "y":
            WorkVacancy(user_input_profession).sort_vacancy()
        WorkVacancy(user_input_profession).top_five_vacancy()
    else:
        pass
    print("Спасибо, что пользуетесь нашим приложением :)")
