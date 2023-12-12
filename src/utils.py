from src.classes import SuperJobAPI, HeadHunterAPI, Vacancy, WriteInfo

def get_vacancy_hh(profession, ):
    hh_api = HeadHunterAPI()
    hh_vacancy = hh_api.get_vacancies(profession)
    vac = Vacancy()
    vac_sort = vac.sorted_vacancies()
    vac_write = WriteInfo().data_write(profession)
def start():
    print("""Приветствую тебя пользователь!!!
             Тебе нужна работа?
             1 - Да, нуждаюсь в работе...
             2 - Не, блатные не работают...""")
    user_input = input()
    if user_input == "2" or user_input == 2:
        pass
    print("""Отлично, в два клика мы сможем подобрать для тебя подходящие вакансии
             Нажми 1 - Подберем для тебя вакансии с сайта hh.ru
             Нажми 2 - Подберем для тебя вакансии с сайта SuperJob
             Нажми 3 - Подберем для тебя вакансии с сайта hh.ru и SuperJob""")
    user_input = input()
    if user_input == "1":




