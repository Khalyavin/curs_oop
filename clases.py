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

    @property
    def get_count_of_vacancy(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        pass


class HHVacancy(Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'HH: ' + super().__str__()


class SJVacancy(Vacancy):  # add counter mixin
    """ SuperJob Vacancy """
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'HH: ' + super().__str__()


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    pass


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    pass