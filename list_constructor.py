import random
from time import sleep
from page_loader import get_page
from link_parser import link_collector
from counter import word_ending_female
from counter import word_ending_male


# Simple function to check whether list of links is already exist as file with given name
# in same folder with parser
# File should have .txt extension. And name should be given without extension
# Also function will check if number of links less that given number
# If file with given name not exist or number of links in file less than given number function will call get_item_list()
# Function returns list of links as list()
# Because parser was used for ozon.ru
# category = '/category/telefony-i-smart-chasy-15501/'
# sorting = '?sorting=rating'
def make_list(name: str = None,
              url: str = '',
              category: str = '',
              sorting: str = '',
              number_required: int = 5,
              pattern: str = '',
              target: str = ''):
    try:
        print(f'Ищу {name}.txt')
        with open(f'{name}.txt') as inf:
            list_of_items = inf.read().splitlines()
    except FileNotFoundError:
        print('Файл не найден')
        print(f'Создаю новый {name}.txt')
        list_of_items = get_item_list(
            url=url, category=category, sorting=sorting,
            pattern=pattern, target=target,
            number_required=number_required, name=name
        )
        return list_of_items
    else:
        if len(list_of_items) < number_required:
            print(f'Файл {name}.txt найден, но количество ссылок меньше {number_required}')
            list_of_items = get_item_list(
                url=url, category=category, sorting=sorting,
                pattern=pattern, target=target,
                number_required=number_required, name=name
            )
            return list_of_items
        else:
            print('Файл найден')
            print('Результат', '\n', len(list_of_items), '\n', "*"*30)
            return list_of_items


# Simple function to rotate pages and collect links
# Function will start from page given in 'page='. If no page number give, function start from first page
# Function will stop rotation when required number of links collected
# Required number of links could be specified in 'number_required=' attribute. By default, it's  5 links
# Function will save list of collected links as .txt in same folder with parser with given name in (name=)
# Function returns list of links as list()
def get_item_list(url: str,
                  category: str = '',
                  sorting: str = '',
                  page: int = 1,
                  number_required: int = 5,
                  name: str = None,
                  pattern: str = '',
                  target: str = ''):
    try:
        list_of_smartphones = []
        while len(list_of_smartphones) < number_required:
            final_url = f'{url+category}?page={str(page)}&{sorting}'  # ulr of page to load and parse
            html = get_page(url=final_url)  # function from page_loader.py
            print('Ищу смартфоны')
            links = link_collector(html=html, pattern=pattern, target=target)  # function from link_parser.py
            list_of_smartphones.extend(list(links))
            print(f'Спарсил - {page} страниц{word_ending_female(page)}')
            print(f'Смартфонов найдено {len(list_of_smartphones)}')
            page += 1
            sleep(round(random.uniform(2.1, 2.5), 2))
        # Saving list of links
        with open(f'{name}.txt', 'w', encoding='utf-8') as f:
            for link in list_of_smartphones:
                f.write(link + '\n')

    except Exception as ex:
        print(ex)
        print(f'Error in {get_item_list.__name__} function')
    else:
        print('Файл создан')
        print(
            'Результат', '\n',
            f'Нашел {len(list_of_smartphones)} смартфон{word_ending_male(len(list_of_smartphones))}',
            '\n', "*"*30
            )
        return list_of_smartphones
