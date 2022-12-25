import engine_classes
import clases
import connector

def main():
    while True:
        print('1. Скачать данные с hh.ru и sj.ru')
        print('2. Сортировать по зарплате')
        print('3. Сортировать по опыту')
        print('4. Просмотр файлов')
        print('[5]. Выход')
        tmp = int(input('Ваш выбор: '))

        if tmp == 1:
            engine_classes.prepare_data()
        elif tmp == 2:
            clases.sorting('sj_res.json')
            clases.sorting('hh_res.json')

            tmp_top = input('Сколько выводить записей? [15] :')

            if not tmp_top:
                tmp_top = 15
            else:
                tmp_top = int(tmp_top)

            clases.get_top('hh_sort.json', 'sj_sort.json', tmp_top)
        elif tmp == 3:
            clases.sorting_experience('hh_res.json')
            clases.sorting_experience('sj_res.json')

            tmp_top = input('Сколько выводить записей? [15] :')

            if not tmp_top:
                tmp_top = 15
            else:
                tmp_top = int(tmp_top)

            clases.get_top_exp('hh_res.json', 'sj_res.json', tmp_top)
        elif tmp == 4:
            while True:
                print('Возможна работа с файлами: ')
                print('1. "hh_res.json"')
                print('2. "hh_sort.json"')
                print('3. "hh_exper.json"')
                print('4. "sj_res.json"')
                print('5. "sj_sort.json"')
                print('6. "sj_exper.json"')
                print('[0]. Возврат в программу')

                tmp_input = input('Ваш выбор: ')

                if not tmp_input:
                    break
                else:
                    tmp_input = int(tmp_input)
                    if tmp_input == 1:
                        engine_classes.get_connector("hh_res.json")
                    elif tmp_input == 2:
                        engine_classes.get_connector("hh_sort.json")
                    elif tmp_input == 3:
                        engine_classes.get_connector("hh_exper.json")
                    elif tmp_input == 4:
                        engine_classes.get_connector("sj_res.json")
                    elif tmp_input == 5:
                        engine_classes.get_connector("sj_sort.json")
                    elif tmp_input == 6:
                        engine_classes.get_connector("sj_exper.json")

                tmp_key = input('Введите поле для поиска: ')
                tmp_value = input('Введите значение для поиска: ')
                tmp_query = {tmp_key: tmp_value}

                print('Методы коннектора: ')
                print('[1]. Поиск по запросу')
                print('2. Удаление по запросу')
                tmp_connect = input('Ваш выбор: ')

                if tmp_connect:
                    if int(tmp_connect) == 2:
                        connector.delete(tmp_query)
                    else:
                        print('Непонятно, чего делать.....')
                else:
                    connector.select(tmp_query)

        else:
            break


if __name__ == '__main__':
    main()