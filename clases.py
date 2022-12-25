import json
from abc import ABC
import requests


class Vacancy(ABC):
    """Класс для работы с зарплатой"""
    usd = 72
    eur = 76

    __slots__ = ('name', 'job', 'link', 'description', 'salary')

    def __init__(self, name, job, link, description, salary):
        self.name = name
        self.job = job
        self.link = link
        self.description = description
        self.salary = salary

    def __str__(self):
        return f'{self.name}, {self.job}, з/п: {self.salary} руб/мес'

    def get_raw_data(self):
        return {
            'name': self.name, 'job': self.job, 'link': self.link, 'description': self.description, 'salary': self.salary
        }

    def __gt__(self, other):
        return self.salary > other

    def __lt__(self, other):
        return self.salary < other

    def __ge__(self, other):
        return self.salary >= other

    def __le__(self, other):
        return self.salary <= other

    def __eq__(self, other):
        return self.salary == other

    def __ne__(self, other):
        return self.salary != other


class Experience(ABC):
    """Класс для работы с опытом"""
    usd = 72
    eur = 76

    def __init__(self, name, job, link, description, salary, experience):
        self.name = name
        self.job = job
        self.link = link
        self.description = description
        self.salary = salary
        self.experience = experience

    def __str__(self):
        return f'{self.name}, {self.job}, з/п: {self.salary} руб/мес, опыт: {self.experience}'

    def get_raw_data(self):
        return {
            'name': self.name,
            'job': self.job,
            'link': self.link,
            'description': self.description,
            'salary': self.salary,
            'experience': self.experience
        }

    def __gt__(self, other):
        return self.experience > other

    def __lt__(self, other):
        return self.experience < other

    def __ge__(self, other):
        return self.experience >= other

    def __le__(self, other):
        return self.experience <= other

    def __eq__(self, other):
        return self.experience == other

    def __ne__(self, other):
        return self.experience != other

class HHExperience(Experience):
    """Данные с hh.ru для парсинга по опыту"""
    def __init__(self, name, job, link, description, salary, experience):
        super().__init__(name, job, link, description, salary, experience)

    def __str__(self):
        return 'HH: ' + super().__str__()

class SJExperience(Experience):
    """Данные с hh.ru для парсинга по опыту"""
    def __init__(self, name, job, link, description, salary, experience):
        super().__init__(name, job, link, description, salary, experience)

    def __str__(self):
        return 'SJ: ' + super().__str__()


class CountMixin:
    def __init__(self, name, job, link, description, salary):
        super().__init__(name, job, link, description, salary)

    #@property
    def get_count_of_vacancy(self, file):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        self.data_file = file
        data = []
        try:
            fp = open(self.data_file, 'r', encoding='utf-8')
        except FileNotFoundError:
            print(f'Скачайте вакансии в файл {self.data_file}')
        else:
            data = json.load(fp)

        fp.close()
        return len(data)


class HHVacancy(Vacancy, CountMixin):  # add counter mixin
    """ HeadHunter Vacancy """
    def __init__(self, name, job, link, description, salary):
        super().__init__(name, job, link, description, salary)

    def __str__(self):
        return 'HH: ' + super().__str__()


class SJVacancy(Vacancy, CountMixin):  # add counter mixin
    """ SuperJob Vacancy """
    def __init__(self, name, job, link, description, salary):
        super().__init__(name, job, link, description, salary)

    def __str__(self):
        return 'SJ: ' + super().__str__()

def sorting(file):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods)
     Сортирует **_res.json в **_sort.json"""

    data = []
    fp = open(file, 'r', encoding='utf-8')
    tmp_data = json.load(fp)
    fp.close()

    if file == 'sj_res.json':
        for object in tmp_data:
            tmp_name = object["client"].get("title")
            tmp_job = object.get("profession")
            tmp_link = object.get("link")
            tmp_description = object.get("work")
            tmp_salary_from = object.get("payment_from")
            tmp_salary_to = object.get("payment_to")
            tmp_salary_curr = object.get("currency")

            tmp_salary = 0
            if tmp_salary_from:
                tmp_salary = tmp_salary_from
            else:
                tmp_salary = tmp_salary_to

            if tmp_salary_curr == 'USD': tmp_salary *= Vacancy.usd
            if tmp_salary_curr == 'EUR': tmp_salary *= Vacancy.eur

            # Данные для десериализации готовы
            sj_vac = SJVacancy(tmp_name, tmp_job, tmp_link, tmp_description, tmp_salary)
            data.append(sj_vac)

    elif file == 'hh_res.json':
        for item in tmp_data:
            tmp_name = item["employer"].get("name")
            tmp_job = item.get("name")
            tmp_link = item.get("alternate_url")
            tmp_description = item["snippet"].get("requirement")
            if item.get("salary"):
                tmp_salary_from = item["salary"].get("from")
                tmp_salary_to = item["salary"].get("to")
                tmp_salary_curr = item["salary"].get("currency")

                tmp_salary = 0
                if tmp_salary_from:
                    tmp_salary = tmp_salary_from
                else:
                    tmp_salary = tmp_salary_to

                if tmp_salary_curr == 'USD': tmp_salary *= Vacancy.usd
                if tmp_salary_curr == 'EUR': tmp_salary *= Vacancy.eur
            else:
                tmp_salary = 0

            # Данные для десериализации готовы
            hh_vac = HHVacancy(tmp_name, tmp_job, tmp_link, tmp_description, tmp_salary)
            data.append(hh_vac)

    data.sort(reverse=True)

    f_name = file.replace('res', 'sort')

    fp = open(f_name, 'w', encoding='utf-8')
    json.dump(data, fp, indent=2, default=lambda o: o.get_raw_data())
    fp.close()

def sorting_experience(file):
    """ Сортирует список вакансий по опыту работы (gt, lt magic methods)
     Сортирует **_res.json в **_expir.json"""

    data = []
    fp = open(file, 'r', encoding='utf-8')
    tmp_data = json.load(fp)
    fp.close()

    if file == 'sj_res.json':
        for object in tmp_data:
            tmp_name = object["client"].get("title")
            tmp_job = object.get("profession")
            tmp_link = object.get("link")
            tmp_description = object.get("work")
            tmp_salary_from = object.get("payment_from")
            tmp_salary_to = object.get("payment_to")
            tmp_salary_curr = object.get("currency")

            tmp_salary = 0
            if tmp_salary_from:
                tmp_salary = tmp_salary_from
            else:
                tmp_salary = tmp_salary_to

            if tmp_salary_curr == 'USD': tmp_salary *= Vacancy.usd
            if tmp_salary_curr == 'EUR': tmp_salary *= Vacancy.eur

            tmp_exp = object["experience"].get("title")

            # Данные для десериализации готовы
            sj_exp = SJExperience(tmp_name, tmp_job, tmp_link, tmp_description, tmp_salary, tmp_exp)
            data.append(sj_exp)

    elif file == 'hh_res.json':
        for item in tmp_data:
            tmp_name = item["employer"].get("name")
            tmp_job = item.get("name")
            tmp_link = item.get("alternate_url")
            tmp_description = item["snippet"].get("requirement")
            if item.get("salary"):
                tmp_salary_from = item["salary"].get("from")
                tmp_salary_to = item["salary"].get("to")
                tmp_salary_curr = item["salary"].get("currency")

                tmp_salary = 0
                if tmp_salary_from:
                    tmp_salary = tmp_salary_from
                else:
                    tmp_salary = tmp_salary_to

                if tmp_salary_curr == 'USD': tmp_salary *= Vacancy.usd
                if tmp_salary_curr == 'EUR': tmp_salary *= Vacancy.eur
            else:
                tmp_salary = 0

            url = 'https://api.hh.ru'
            vac_id = item.get("id")
            url += '/vacancies/' + vac_id
            responce = requests.request("GET", url)
            if responce.status_code == 200:
                tmp_exp = responce.json()['experience'].get('name')

            # Данные для десериализации готовы
            hh_exp = HHExperience(tmp_name, tmp_job, tmp_link, tmp_description, tmp_salary, tmp_exp)
            print(hh_exp)
            data.append(hh_exp)

    data.sort(reverse=False)

    f_name = file.replace('res', 'exper')

    fp = open(f_name, 'w', encoding='utf-8')
    json.dump(data, fp, indent=2, default=lambda o: o.get_raw_data())
    fp.close()


def get_top(hh_file, sj_file, top_count):
    """ Возвращает {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    hh_fp = open(hh_file, 'r', encoding='utf-8')
    sj_fp = open(sj_file, 'r', encoding='utf-8')
    hh_data = json.load(hh_fp)
    sj_data = json.load(sj_fp)
    hh_fp.close()
    sj_fp.close()

    tmp_cntr = 0
    hh_cntr = 0
    sj_cntr = 0

    while tmp_cntr <= top_count:
        tmp_cntr += 1
        if int(hh_data[hh_cntr]["salary"]) > int(sj_data[sj_cntr]["salary"]):
            print(f'HH: {hh_data[hh_cntr]["name"]}. {hh_data[hh_cntr]["job"]}. З/п {hh_data[hh_cntr]["salary"]} в мес.')
            print(f'    {hh_data[hh_cntr]["link"]} {hh_data[hh_cntr]["description"]}')
            hh_cntr += 1
        else:
            print(f'SJ: {sj_data[sj_cntr]["name"]}. {sj_data[sj_cntr]["job"]}. З/п {sj_data[sj_cntr]["salary"]} в мес.')
            print(f'    {sj_data[sj_cntr]["link"]} {sj_data[sj_cntr]["description"]}')
            sj_cntr += 1

def get_top_exp(hh_file, sj_file, top_count):
    """ Возвращает {top_count} записей из вакансий по опыту работы (iter, next magic methods) """
    hh_fp = open(hh_file, 'r', encoding='utf-8')
    sj_fp = open(sj_file, 'r', encoding='utf-8')
    hh_data = json.load(hh_fp)
    sj_data = json.load(sj_fp)
    hh_fp.close()
    sj_fp.close()

    tmp_cntr = 0
    hh_cntr = 0
    sj_cntr = 0

    while tmp_cntr <= top_count:
        tmp_cntr += 1
        if hh_data[hh_cntr]["experience"] > sj_data[sj_cntr]["experience"]:
            print(f'HH: {hh_data[hh_cntr]["name"]}. {hh_data[hh_cntr]["job"]}. З/п {hh_data[hh_cntr]["salary"]} в мес.')
            print(f'    {hh_data[hh_cntr]["experience"]} {hh_data[hh_cntr]["link"]} {hh_data[hh_cntr]["description"]}')
            hh_cntr += 1
        else:
            print(f'SJ: {sj_data[sj_cntr]["name"]}. {sj_data[sj_cntr]["job"]}. З/п {sj_data[sj_cntr]["salary"]} в мес.')
            print(f'    {sj_data[sj_cntr]["experience"]} {sj_data[sj_cntr]["link"]} {sj_data[sj_cntr]["description"]}')
            sj_cntr += 1


if __name__ == '__main__':
    # sorting('sj_res.json')
    # sorting('hh_res.json')
    # get_top('hh_sort.json', 'sj_sort.json', 15)

    # sorting_experience('hh_res.json')
    # sorting_experience('sj_res.json')
    get_top_exp('hh_exper.json', 'sj_exper.json', 15)
