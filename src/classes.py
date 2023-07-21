from abc import ABC
import json
import requests


class API(ABC):
    def __init__(self, key):
        self.key = key
        self.vacansies = []


class HH(API):

    def get_request(self):
        """Собирает вакансии по ключевому слову"""
        for page in range(10):
            url = "https://api.hh.ru/vacancies"
            params = {
                "per_page": 100,
                "page": page,
                "text": self.key,
                "archive": False
            }
            response = requests.get(url, params=params).json()
            self.vacansies.extend(response['items'])

    def get_formatted_vacancies(self):
        """Возвращает вакансии с зарплатой в рублях"""
        formatted_vacansies = []
        for vacansy in self.vacansies:
            if vacansy['salary'] is not None:
                if vacansy['salary']['currency'] == 'RUR':
                    formatted_vacansies.append({
                        'name': vacansy['name'],
                        'area': vacansy['area']['name'],
                        'salary_from': vacansy['salary']['from'],
                        'salary_to': vacansy['salary']['to'],
                        'url': vacansy['alternate_url'],
                        'employer': vacansy['employer']['name'],
                        'requirement': vacansy['snippet']['requirement'],
                    })
        return formatted_vacansies


class Superjob(API):

    def get_request(self):
        """Собирает вакансии по ключевому слову"""
        for page in range(10):
            url = "https://api.superjob.ru/2.0/vacancies/"
            parametr = {
                "count": 1000,
                "page": page,
                "keyword": self.key,
                "archive": False
            }
            headers = {
                "X-Api-App-Id": "v3.r.137694851.146a23e73bd9e59150c0105879f8017913a39b86"
                                ".b6b0a759a7c84c058bf9c757bc5bbfc0c40911d9 "
            }
            response = requests.get(url, headers=headers, params=parametr).json()
            self.vacansies.extend(response['objects'])

    def get_formatted_vacancies(self):
        formatted_vacansies = []
        for vacansy in self.vacansies:
            if vacansy['currency'] == 'rub':
                formatted_vacansies.append({
                    'name': vacansy['profession'],
                    'area': vacansy['town']['title'],
                    'salary_from': vacansy['payment_from'],
                    'salary_to': vacansy['payment_to'],
                    'url': vacansy['link'],
                    'employer': vacansy['firm_name'],
                    'requirement': vacansy['candidat'],
                })

        return formatted_vacansies


class Vacancy:

    def __init__(self, vacansy):
        self.name = vacansy['name']
        self.area = vacansy['area']
        if vacansy['salary_from'] is None:
            self.salary_from = 0
        else:
            self.salary_from = vacansy['salary_from']
        if vacansy['salary_to'] is None:
            self.salary_to = 0
        else:
            self.salary_to = vacansy['salary_to']
        self.url = vacansy['url']
        self.employer = vacansy['employer']
        self.requirement = vacansy['requirement']

    def __gt__(self, other):
        """Сравнение вакансий по мин зарплате"""
        return self.salary_from > other.salary_from

    def __str__(self):
        return f"""
        {self.name}, {self.area}
        Зарплата от {self.salary_from} до {self.salary_to} руб.
        {self.url}
        """


class JSON:
    """Сохранение информации о вакансиях в JSON-файл"""

    def __init__(self, filename, vacansies):
        self.filename = filename
        self.create_file(vacansies)

    def create_file(self, vacansies):

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(vacansies, f, indent=2, ensure_ascii=False)

    def all_data(self):

        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        vacansy_data = []
        for x in data:
            vacansy_data.append(Vacancy(x))
        return vacansy_data

    def sorted_by_salary(self):
        """Сортирует вакансии по возрастанию зарплаты"""

        data = self.all_data()
        d = sorted(data)
        return d
