import json
import requests
from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):
    __url = 'https://api.hh.ru'
    __per_page = 20

    def _get_vacancies(self, search_word, page):
        print(f'Try to get from hh.ru page number: {page + 1}')
        responce = requests.get(f'{self.__url}/vacancies?text={search_word}&page={page}')
        if responce.status_code == 200:
            return responce.json()

        return None

    def get_request(self, search_word, vacancies_count):
        page = 0
        result = []
        while self.__per_page * page < vacancies_count:
            tmp_result = self._get_vacancies(search_word, page)
            if tmp_result:
                result += tmp_result.get('items')
                page += 1
            else:
                break

        return result


class SuperJob(Engine):
    __url = 'https://api.superjob.ru/2.0'
    __key = 'v3.r.129863982.c889b7015220a7f8a8976eccba85e22445dfe88e.0e1b4bcb3588b68bf13d37b08aedb02499b70256'
    __per_page = 20

    def _send_request(self, search_word, page):
        url = f'{self.__url}/vacancies/?page={page}&reyword={search_word}'

        headers = {
            'X-Api-App-Id': self.__key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        responce = requests.get(
            url=url,
            headers=headers
        )
        if responce.status_code == 200:
            return responce.json()

        return None


    def get_request(self, search_word, vacancies_count):
        page = 0
        result = []
        while self.__per_page * page < vacancies_count:
            tmp_result = self._get_vacancies(search_word, page)
            if tmp_result:
                result += tmp_result.get('objects')
                page += 1
            else:
                break

        return result


if __name__ == '__main__':
    # hh_engine = HH()
    # search_word = 'Python'
    # vacancies_count = 100
    #
    # result = hh_engine.get_request(search_word, vacancies_count)
    # print(len(result))
    #
    # with open('hh_res.json', 'w', encoding='utf-8') as res_file:
    #     json.dump(result, res_file)
    #
    # with open('hh_res.json', 'r', encoding='utf-8') as res_file:
    #     res_data = json.load(res_file)
    #     for item in res_data:
    #         print(f'{item.get("name")}, {item["url"]}, {item.get("salary")}), {item["schedule"].get("name")}, \n    '
    #               f'{item["snippet"].get("requirement")}, {item["area"].get("name")}')

    sj_engine = SuperJob()
    search_word = 'Python'
    vacancies_count = 100

    result = sj_engine.get_request(search_word, vacancies_count)

    with open('sj_res.json', 'w', encoding='utf-8') as res_file:
        json.dump(result, res_file)
