import json
from abc import ABC


class Vacancy(ABC):
    __slots__ = ('name', 'job', 'link', 'description', 'salary')

    def __init__(self, name, job, link, description, salary):
        self.name = name
        self.job = job
        self.link = link
        self.description = description
        self.salary = salary
        self.usd = 72
        self.eur = 76

    def __str__(self):
        return f'{self.name}, {self.job}, з/п: {self.salary} руб/мес'

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

    def get_raw_data(self):
        return {
            'name': self.name, 'job': self.job, 'lnk': self.link, 'description': self.description, 'salary': self.salary
        }

    def sorting(self):
        """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods)
         Сортирует sj_res.json в sj_sort.json"""

        data = []
        fp = open('sj_res.json', 'r', encoding='utf-8')
        tmp_data = json.load(fp)
        fp.close()

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

            if tmp_salary_curr == 'usd': tmp_salary *= self.usd
            if tmp_salary_curr == 'eur': tmp_salary *= self.eur

            # Данные для десериализации готовы
            sj_vac = SJVacancy(tmp_name, tmp_job, tmp_link, tmp_description, tmp_salary)
            data.append(sj_vac)

        data.sort(reverse=True)

        fp = open('sj_sort.json', 'w', encoding='utf-8')
        json.dump(data, fp, indent=2, ensure_ascii=False, default=lambda o: o.get_raw_data())
        fp.close()



def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    pass


if __name__ == '__main__':
    SJVacancy.sorting('sj_res.json')
