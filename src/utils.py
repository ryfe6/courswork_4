from data_load import Request
from logger import setup_logging

logger = setup_logging


class HeadHunterAPI(Request):
    def __init__(self, profession, url):
        super().__init__(profession, url)


class SuperJobAPI(Request):
    pass


url = 'https://api.hh.ru/vacancies'
print(HeadHunterAPI('python', url))
