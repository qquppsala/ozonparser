import re
from bs4 import BeautifulSoup


# Simple function to parse page for OS_data using BS4
# Functon will parse given html(as string)
# Function will return dict() of items
# Because function was used to parse ozon.ru, pattern and target "tuned" for ozon.ru pages
# Function was used to parse for 'Версия' which given as target
# You cant try to change target to parse another item
# All items on ozon.ru was under tag = <div class='widget-search-result-container'...
# So such pattern was used
def data_collector(html: str, target: str):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        item = soup.find('span', text=re.compile(target)).find_next('dd').get_text()
    except Exception as ex:
        print("-"*30)
        print(ex)
        print(f'Error in {data_collector.__name__} function')
        print('Возможно ОС не указана. В словарь внесен ключ "ОС не указана"')
        print("-"*30)
        return "ОС не указана"
    else:
        return item
