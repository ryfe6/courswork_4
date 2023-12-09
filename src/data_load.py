import requests
import json
import time
import os
from abc import ABC, abstractmethod
from logger import setup_logging
logger = setup_logging


class Request(ABC):
    def __init__(self, profession, url, page=0):
        self.profession = profession
        self.url = url
        self.page = page


    @abstractmethod
    def get_page(self):
        logger.info("Функция get_page начала свою работу")
        params = {'text': f'NAME:{self.profession}',
                  'page': self.page,
                  'per_page': 100
                  }

        req = requests.get(self.url, params)
        data = req.content.decode()
        req.close()
        with open('data_json.json', 'w', encoding='utf8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))
            time.sleep(0.25)
        logger.info("Функция get_page закончила свою работу с результатом 0")


    # for page in range(0, 2):
    #     js_obj = json.loads(get_page("python"))
    #     #nextFileName = 'data_json.json'.format(len(os.listdir('../src')))
    #
    #     with open('data_json.json', 'w', encoding='utf8') as file:
    #         file.write(json.dumps(js_obj, indent=2, ensure_ascii=False))
    #         time.sleep(0.25)