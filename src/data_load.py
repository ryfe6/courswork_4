import requests
import json
import time
import os


def get_page(profession, page=0):
    params = {'text': f'NAME:{profession}',
              'page': page,
              'per_page': 100
              }

    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()
    return data


for page in range(0, 20):
    js_obj = json.loads(get_page("python"))
    with open('data_json.json', 'a', encoding='utf8') as file:
        file.write(json.dumps(js_obj, ensure_ascii=False))