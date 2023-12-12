import os

from src.data_load import Request, DataWrite
from src.logger import setup_logging
import requests
import json
import time

logger = setup_logging()


class HeadHunterAPI(Request):
    vacancies_dicts_hh = []

    def get_vacancies(self, profession, page=0):
        logger.info("Функция get_page_in_hh начала свою работу")
        params = {'text': f'NAME:{profession}',
                  'page': page,
                  'per_page': 100
                  }
        req = requests.get(url='https://api.hh.ru/vacancies', params=params)
        data = req.json()
        req.close()
        time.sleep(0.25)
        vacancies = data['items']
        for vacancy in vacancies:
            if vacancy['salary'] is not None and vacancy['salary']['currency'] == "RUR":
                vacancy_dict = {'employer': vacancy['employer']['name'], 'name': vacancy['name'],
                                'url': vacancy['apply_alternate_url'], 'requirement': vacancy['snippet']['requirement'],
                                'salary_from': vacancy['salary']['from'], 'salary_to': vacancy['salary']['to']
                                }
                if vacancy_dict['salary_from'] is None:
                    vacancy_dict['salary_from'] = 0
                elif vacancy_dict['salary_to'] is None:
                    vacancy_dict['salary_to'] = vacancy_dict['salary_from']
                self.vacancies_dicts_hh.append(vacancy_dict)
        logger.info("Функция get_page_in_hh закончила свою работу с результатом 0")


class SuperJobAPI(Request):
    sj_api_key = os.getenv("SJ_API_KEY")
    vacancy_dicts_sj = []

    def __init__(self):
        self.headers = {'X-Api-App-Id': self.sj_api_key}

    def get_vacancies(self, profession, page=0):
        logger.info("Функция get_page_in_sj начала свою работу")
        params = {"keyword": profession,
                  'page': page,
                  'count': 100}
        req = requests.get(url='https://api.hh.ru/vacancies', headers=self.headers, params=params)
        data = req.json()
        req.close()
        time.sleep(0.25)
        vacancies = data['objects']
        for vacancy in vacancies:
            try:
                if vacancy['payment_from'] != 0 and vacancy['payment_to'] != 0 and vacancy['currency'] == "rub":
                    vacancy_dict = {'employer': vacancy['client']['title'], 'name': vacancy['profession'],
                                    'url': vacancy['link'], 'requirement': vacancy['candidat'],
                                    'salary_from': vacancy['payment_from'], 'salary_to': vacancy['payment_to']}
                    if vacancy_dict['salary_to'] == 0:
                        vacancy_dict['salary_to'] = vacancy_dict['salary_from']
                    self.vacancy_dicts_sj.append(vacancy_dict)
            except KeyError:
                continue
        logger.info("Функция get_page_in_sj закончила свою работу с результатом 0")


class Vacancy(SuperJobAPI, HeadHunterAPI):
    new_vacancy = []

    def __init__(self, name=None, url=None, pay_to=None, pay_from=None, texting=None):
        super().__init__()
        self.vacancy_dict = self.vacancy_dicts_sj + self.vacancies_dicts_hh
        self.name = name
        self.url = url
        self.pay_to = pay_to
        self.pay_from = pay_from
        self.texting = texting

    def sorted_vacancies(self):
        for vacancy in self.vacancy_dict:
            if self.name is None or self.name in vacancy['name'].lower():
                if self.url is None or self.url in vacancy['url']:
                    if self.texting is None or self.texting in vacancy['requirement'].lower():
                        if self.pay_from is None or self.pay_from <= vacancy['salary_from']:
                            if self.pay_to is None or self.pay_to >= vacancy['salary_to']:
                                self.new_vacancy.append(vacancy)
        if len(self.new_vacancy) >= 1:
            print("Отбор прошёл успешно")
        else:
            print("Нет нужных данных")


class WriteInfo(DataWrite, Vacancy):

    def data_write(self, profession):
        with open(f"{profession}.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(self.new_vacancy, indent=2, ensure_ascii=False))




