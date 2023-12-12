import requests
import json
import time
import os
from abc import ABC, abstractmethod
from src.logger import setup_logging
logger = setup_logging


class Request(ABC):

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass


class DataWrite:

    @abstractmethod
    def data_write(self, *args, **kwargs):
        pass


    # for page in range(0, 2):
    #     js_obj = json.loads(get_page("python"))
    #     #nextFileName = 'data_json.json'.format(len(os.listdir('../src')))
    #
    #     with open('data_json.json', 'w', encoding='utf8') as file:
    #         file.write(json.dumps(js_obj, indent=2, ensure_ascii=False))
    #         time.sleep(0.25)