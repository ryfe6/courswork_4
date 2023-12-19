import json
import os
import time
from typing import Any

import requests

from src.abstract_class import DataWrite, Request
from src.logger import setup_logging

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
        print("Начинаем загрузку данных...")
        for i in range(10):
            params = {"text": profession, "page": page, "per_page": 100}
            headers = {"User-Agent": "Your User Agent"}
            req = requests.get(url="https://api.hh.ru/vacancies", params=params, headers=headers)
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
            print("Не удалось получить данные, проверьте соединение с интернетом...")
        else:
            print("Данные получены")
        logger.info("Функция get_page_in_hh закончила свою работу")


class SuperJobAPI(Request):
    """Класс для работы с API сайта SuperJob"""

    sj_api_key = os.getenv("SJ_API_KEY")
    vacancy_dicts_sj: list = []

    def __init__(self) -> None:
        self.headers = {"X-Api-App-Id": self.sj_api_key}
        super().__init__()

    def get_vacancies(self, profession: str, page: int = 0) -> None:
        """
        Метод get_vacancies отправляет запрос на сайт SuperJob и получает данные, обрабатывает и убирает
        в список self.vacancy_dicts_sj.
        :param profession: Профессия, которую задает пользователь для поиска вакансий.
        :param page: Номер страницы с которой начинается поиск.
        """
        logger.info("Функция get_page_in_sj начала свою работу")
        print("Начинаем загрузку данных...")
        for i in range(10):
            params = {"keyword": profession, "page": page, "count": 100}
            req = requests.get(url="https://api.superjob.ru/2.0/vacancies", headers=self.headers, params=params)
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
            print("Не удалось получить данные, проверьте соединение с интернетом...")
        else:
            print("Данные получены")
        logger.info("Функция get_page_in_sj закончила свою работу")


class Vacancy(SuperJobAPI, HeadHunterAPI):
    """Класс для работы и редактирования данных вакансий."""

    new_vacancy: list = []

    def __init__(self, name: Any = None, url: Any = None, pay_to: Any = None, pay_from: Any = None, texting: Any = None,):
        super().__init__()
        self.vacancy_dict = self.vacancy_dicts_sj + self.vacancies_dicts_hh
        self.name = name
        self.url = url
        self.pay_to = pay_to
        self.pay_from = pay_from
        self.texting = texting

    def sorted_vacancies(self) -> None:
        """Метод для фильтрации вакансий."""
        logger.info("Функция sorted_vacancies начала свою работу")
        for vacancy in self.vacancy_dict:
            if self.name is None or self.name in vacancy["name"].lower():
                if self.url is None or self.url in vacancy["url"]:
                    if self.texting is None or self.texting in vacancy["requirement"].lower():
                        if self.pay_from is None or self.pay_from <= vacancy["salary_from"]:
                            if self.pay_to is None or self.pay_to >= vacancy["salary_to"]:
                                self.new_vacancy.append(vacancy)
        logger.info("Функция sorted_vacancies закончила свою работу")


class WriteInfo(DataWrite, Vacancy):
    """Класс для записи данных о полученных вакансиях в файл."""

    def data_write(self, profession: str) -> None:
        """
        Метод записывает в json файл полученные вакансии и их данные
        :param profession: Профессия для которой будет создан json файл.
        """
        logger.info("Функция data_write начала свою работу")
        with open(f"../data/{profession}.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(self.new_vacancy, indent=2, ensure_ascii=False))
        logger.info("Функция data_write закончила свою работу")
