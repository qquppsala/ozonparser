import json
from page_loader import get_page
from data_parser import data_collector
from counter import word_ending_male


# Simple function to check whether data is already exist as file with given name
# in same folder with parser
# File should have .json extension. And name should be given without extension
# If file with given name not exist function will call get_data() to create one
# Function saves json by default, if you don't need one just do (save = False)
# Function returns data as dict()
# Because parser was used for ozon.ru some tuning was done on called functions
def make_json(some_list: list, url: str = '', name: str = 'Json', target: str = 'Версия'):
    try:
        print(f'Ищу {name}.json')
        with open(f'{name}.json') as inf:
            data = json.load(inf)
    except FileNotFoundError:
        print('Файл не найден')
        print(f'Создаю новый {name}.json')
        data = get_data(some_list, url, name, target)
        return data
    else:
        print('Файл найден')
        print('Результат', '\n', data, '\n', "*"*30)
        return data


# Simple function to run pages from given list and collect data
# Function will save data as .json in same folder with parser with given name in (name=)
# Function returns data as dict()
def get_data(_list: list, url: str = '', name: str = 'Json', target: str = 'Версия', save=True):
    data = {}
    i = 0
    try:
        for link in _list:
            print('Парсим данные смартфонов')
            final_url = f'{url+link}features/'
            html = get_page(url=final_url, name=name, save=True)  # function from page_loader.py
            item = data_collector(html=html, target=target)  # function from data_parser.py
            if item not in data.keys():
                data.update({f'{item}': 1})
            else:
                data[item] += 1
            i += 1
            print(f'Проверил -  {i} смартфон{word_ending_male(i)}')
            print(f'Промежуточный результат{data}')
        if save:
            with open(f'{name}.json', 'w') as ouf:
                json.dump(data, ouf)
    except Exception as ex:
        print(ex)
        print(f'Error in {get_data.__name__} function')
    else:
        print('Файл создан')
        print('Финальный результат', '\n', data, '\n', "*"*30)
        return data
