import re
from bs4 import BeautifulSoup


# Simple function to parse page for links using BS4
# Functon will parse given html(as string)
# Function will return set() of links
# Because function was used to parse ozon.ru, pattern and target "tuned" for ozon.ru pages
# Function was used to parse for 'Смартфон' which given as target
# You cant try to change target to parse another item
# All items on ozon.ru was under tag = <div class='widget-search-result-container'...
# So such pattern was used
def link_collector(html: str, pattern: str, target: str):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        items = soup.find(
            'div', attrs={'class': f'{pattern}'}
        ).find_all('a', text=re.compile(target))
        for item in items:
            links.append(item.get('href').split('?')[0])
    except Exception as ex:
        print(ex)
        print(f'Error in {link_collector.__name__} function')
    else:
        return set(links)
