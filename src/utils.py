import logging

from src.classes import SuperJobAPI, HeadHunterAPI, Vacancy, WriteInfo
import json


def get_vacancy(script: str, profession: str) -> None:
    """
    Функция С помощью полученных данных запускает один из трех сценариев
    :param script: Номер сценария
    :param profession: Имя профессии
    :return: None
    """
    if script == "1":
        hh_api = HeadHunterAPI()
        hh_vacancy = hh_api.get_vacancies(profession)
    elif script == "2":
        sj_api = SuperJobAPI()
        sj_vacancy = sj_api.get_vacancies(profession)
    elif script == "3":
        hh_api = HeadHunterAPI()
        sj_api = SuperJobAPI()
        hh_vacancy = hh_api.get_vacancies(profession)
        sj_vacancy = sj_api.get_vacancies(profession)


def sort_vacancy_and_write(profession: str, list_params: list = None) -> None:
    vac = Vacancy(list_params[0], list_params[1], list_params[2], list_params[3], list_params[4])
    vac_sort = vac.sorted_vacancies()
    vac_write = WriteInfo().data_write(profession)


def parameters(name: str, url: str, pay_to: str, pay_from: str, texting: str) -> list:
    param_d = [name, url, pay_to, pay_from, texting]
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


def start():
    print(
        """Приветствую тебя пользователь!!!
             Тебе нужна работа?
             1 - Да, нуждаюсь в работе...
             2 - Не, блатные не работают..."""
    )
    user_input = input()
    if user_input == "2":
        pass
    elif user_input == "1":
        print("""Введите имя профессии, чтобы подобрать нужные вакансии""")
        user_input_profession = input()
        print(
            """Отлично, в два клика мы сможем подобрать для тебя подходящие вакансии
                 Нажми 1 - Подберем для тебя вакансии с сайта hh.ru
                 Нажми 2 - Подберем для тебя вакансии с сайта SuperJob
                 Нажми 3 - Подберем для тебя вакансии с сайта hh.ru и SuperJob"""
        )
        user_input = input()
        if user_input == "1":
            get_vacancy("1", user_input_profession)
        elif user_input == "2":
            get_vacancy("2", user_input_profession)
        elif user_input == "3":
            get_vacancy("3", user_input_profession)
        else:
            print("Жаль, что мы не смогли вам помочь найти работу :(")
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
            user_input_requirement = input("Напишите описание вакансии - ")
            params = parameters(
                name=user_input_name,
                url=user_input_url,
                pay_to=user_input_pay_to,
                pay_from=user_input_pay_from,
                texting=user_input_requirement,
            )
            sort_vacancy_and_write(user_input_profession, params)
        elif user_input == "n":
            params = [None, None, None, None, None]
            sort_vacancy_and_write(user_input_profession, params)
        print(f"""Данные сохранены в файл {user_input_profession}.json""")
