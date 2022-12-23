import json
from abc import ABC


class Vacancy(ABC):
    __slots__ = ('name', 'link', 'description', 'salary')

    def __init__(self, name, job, link, description, salary):
        self.name = name
        self.job = job
        self.link = link
        self.description = description
        self.salary = salary

    def __str__(self):
        return f'{self.name}, {self.job}, з/п: {self.salary} руб/мес'


class CountMixin:

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
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'HH: ' + super().__str__()

    def count_of_vacancies(self):
        return f'От сервиса hh.ru получено {self.count_of_vacancies("hh_res.json")} вакансий.'


class SJVacancy(Vacancy, CountMixin):  # add counter mixin
    """ SuperJob Vacancy """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'HH: ' + super().__str__()

    def count_of_vacancies(self):
        return f'От сервиса sj.ru получено {self.count_of_vacancies("sj_res.json")} вакансий.'


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    pass


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    pass