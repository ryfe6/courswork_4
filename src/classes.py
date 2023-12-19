import json
import time
from os import getenv
from typing import Any

import requests
from dotenv import find_dotenv, load_dotenv

from src.abstract_class import DataWrite, Request
from src.logger import setup_logging

load_dotenv(find_dotenv())
load_dotenv()

logger = setup_logging()


class HeadHunterAPI(Request):
    """Класс для работы с API сайта HeadHunter"""

    vacancies_dicts_hh: list = []

    def get_vacancies(self, profession: str, page: int = 0) -> None:
        """
        Метод get_vacancies отправляет запрос на сайт HeadHunter и получает данные, обрабатывает и убирает
        в список self.vacancies_dicts_hh.
        :param profession: Профессия, которую задает пользователь для поиска вакансий.
        :param page: Номер страницы с которой начинается поиск.
        """
        logger.info("Функция get_page_in_hh начала свою работу")
        print("Начинаем загрузку данных с сайта HeadHunter...")
        for i in range(10):
            params = {"text": profession, "page": page, "per_page": 100}
            headers = {"User-Agent": "Your User Agent"}
            req = requests.get(url=getenv("HH_URL"), params=params, headers=headers)
            data = req.json()
            req.close()
            time.sleep(0.25)
            vacancies = data["items"]
            for vacancy in vacancies:
                if vacancy["salary"] is not None and vacancy["salary"]["currency"] == "RUR":
                    vacancy_dict = {
                        "employer": vacancy["employer"]["name"],
                        "name": vacancy["name"],
                        "url": vacancy["apply_alternate_url"],
                        "requirement": vacancy["snippet"]["requirement"],
                        "salary_from": vacancy["salary"]["from"],
                        "salary_to": vacancy["salary"]["to"],
                    }
                    if vacancy_dict["salary_from"] is None:
                        vacancy_dict["salary_from"] = 0
                    elif vacancy_dict["salary_to"] is None:
                        vacancy_dict["salary_to"] = vacancy_dict["salary_from"]
                    self.vacancies_dicts_hh.append(vacancy_dict)
            page += 1
        if len(self.vacancies_dicts_hh) == 0:
            print("Не удалось получить данные с сайта HeadHunter, проверьте соединение с интернетом...")
        else:
            print("Данные получены")
        logger.info("Функция get_page_in_hh закончила свою работу")


class SuperJobAPI(Request):
    """Класс для работы с API сайта SuperJob"""

    # sj_api_key = os.environ["API_SJ"]
    vacancy_dicts_sj: list = []
    # url_sj = os.environ['SJ_URL']

    def __init__(self) -> None:
        self.headers = {"X-Api-App-Id": getenv("API_SJ")}
        super().__init__()

    def get_vacancies(self, profession: str, page: int = 0) -> None:
        """
        Метод get_vacancies отправляет запрос на сайт SuperJob и получает данные, обрабатывает и убирает
        в список self.vacancy_dicts_sj.
        :param profession: Профессия, которую задает пользователь для поиска вакансий.
        :param page: Номер страницы с которой начинается поиск.
        """
        logger.info("Функция get_page_in_sj начала свою работу")
        print("Начинаем загрузку данных с сайта SuperJob...")
        for i in range(10):
            params = {"keyword": profession, "page": page, "count": 100}
            req = requests.get(url=getenv("SJ_URL"), headers=self.headers, params=params)
            data = req.json()
            req.close()
            time.sleep(0.25)
            vacancies = data["objects"]
            for vacancy in vacancies:
                try:
                    if vacancy["payment_from"] != 0 and vacancy["payment_to"] != 0 and vacancy["currency"] == "rub":
                        vacancy_dict = {
                            "employer": vacancy["client"]["title"],
                            "name": vacancy["profession"],
                            "url": vacancy["link"],
                            "requirement": vacancy["candidat"],
                            "salary_from": vacancy["payment_from"],
                            "salary_to": vacancy["payment_to"],
                        }
                        if vacancy_dict["salary_to"] == 0:
                            vacancy_dict["salary_to"] = vacancy_dict["salary_from"]
                        self.vacancy_dicts_sj.append(vacancy_dict)
                except KeyError:
                    continue
            page += 1
        if len(self.vacancy_dicts_sj) == 0:
            print("Не удалось получить данные с сайта SuperJob, проверьте соединение с интернетом...")
        else:
            print("Данные получены")
        logger.info("Функция get_page_in_sj закончила свою работу")


class Vacancy(SuperJobAPI, HeadHunterAPI):
    """Класс для работы и редактирования данных вакансий."""

    new_vacancy: list = []

    def __init__(
        self,
        name: Any = None,
        url: Any = None,
        pay_to: Any = None,
        pay_from: Any = None,
        requirement: Any = None,
    ):
        super().__init__()
        self.vacancy_dict = self.vacancy_dicts_sj + self.vacancies_dicts_hh
        self.name = name
        self.url = url
        self.pay_to = pay_to
        self.pay_from = pay_from
        self.requirement = requirement

    def filter_vacancies(self) -> None:
        """Метод filter_vacancies, применяет фильтр к полученным вакансиям."""
        logger.info("Функция sorted_vacancies начала свою работу")
        if self.name == "":
            self.name = None
        if self.url == "":
            self.url = None
        if self.requirement == "":
            self.requirement = None
        try:
            self.pay_to = int(self.pay_to)
        except Exception as e:
            self.pay_to = None
            logger.info(e)
        try:
            self.pay_from = int(self.pay_from)
        except Exception as e:
            self.pay_from = None
            logger.info(e)
        for vacancy in self.vacancy_dict:
            if self.name is None or self.name in vacancy["name"].lower():
                if self.url is None or self.url in vacancy["url"]:
                    if self.requirement is None or self.requirement in vacancy["requirement"].lower():
                        if self.pay_from is None or self.pay_from <= vacancy["salary_from"]:
                            if self.pay_to is None or self.pay_to >= vacancy["salary_to"]:
                                self.new_vacancy.append(vacancy)
        logger.info("Функция sorted_vacancies закончила свою работу")


class WriteInfo(DataWrite, Vacancy):
    """Класс для записи данных о полученных вакансиях в файл."""

    def __init__(self, profession: str) -> None:
        super().__init__()
        self.profession = profession

    def data_write(self) -> None:
        """Метод записывает в json файл полученные вакансии и их данные"""
        logger.info("Функция data_write начала свою работу")
        with open(f"../data/{self.profession}.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(self.new_vacancy, indent=2, ensure_ascii=False))
        logger.info("Функция data_write закончила свою работу")


class WorkVacancy(WriteInfo):
    """Класс для работы с вакансиями."""

    def __init__(self, profession: str) -> None:
        super().__init__(profession)
        self.profession = profession

    def bf_print(self) -> None:
        """Метод преобразует данные в красивый вид, эти данные выводятся пользователь на экран."""
        logger.info("Функция bf_print начала свою работу")
        with open(f"../data/{self.profession}.json", "r", encoding="utf8") as file:
            json_file = json.load(file)
            for line in json_file:
                print(
                    f"Заказчик: {line['employer']}\n"
                    f"Имя профеcсии: {line['name']}\n"
                    f"Ссылка на профессию: {line['url']}\n"
                    f"Описание вакансии: {line['requirement']}\n"
                    f"Зарплата от: {line['salary_from']}\n"
                    f"Зарплата до: {line['salary_to']}\n"
                )
        logger.info("Функция bf_print закончила свою работу")

    def sort_vacancy(self) -> None:
        """Метод сортирует вакансии по уменьшению заработной платы"""
        logger.info("Функция sort_vacancy начала свою работу")
        with open(f"../data/{self.profession}.json", "r", encoding="utf-8") as file:
            json_file = json.load(file)
            sort = sorted(json_file, key=lambda x: x["salary_to"], reverse=True)

        with open(f"../data/{self.profession}.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(sort, indent=2, ensure_ascii=False))
        logger.info("Функция sort_vacancy закончила свою работу")

    def top_five_vacancy(self) -> None:
        """Метод выводит в отдельный файл 5 самых высокооплачиваемых вакансий."""
        logger.info("Функция top_five_vacancy начала свою работу")
        with open(f"../data/{self.profession}.json", "r", encoding="utf8") as file:
            json_file = json.load(file)
            top_vacancy = json_file[0:5]
        with open(f"../data/top_{self.profession}.json", "w", encoding="utf8") as file:
            file.write(json.dumps(top_vacancy, indent=2, ensure_ascii=False))
        print(f"Данные выведены в файл ../data/top_{self.profession}.json")
        logger.info("Функция top_five_vacancy закончила свою работу")
