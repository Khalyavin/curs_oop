import json
from abc import ABC


class Vacancy(ABC):
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
     Сортирует sj_res.json в sj_sort.json"""

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
            print(f'    {hh_data[hh_cntr]["link"]}{hh_data[hh_cntr]["description"]}')
            hh_cntr += 1
        else:
            print(f'SJ: {sj_data[sj_cntr]["name"]}. {sj_data[sj_cntr]["job"]}. З/п {sj_data[sj_cntr]["salary"]} в мес.')
            print(f'    {sj_data[sj_cntr]["link"]} {sj_data[sj_cntr]["description"]}')
            sj_cntr += 1



if __name__ == '__main__':
    sorting('sj_res.json')
    sorting('hh_res.json')
    get_top('hh_sort.json', 'sj_sort.json', 15)
