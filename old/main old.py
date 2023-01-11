import random
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt

url = 'https://www.ozon.ru'
category = '/category/telefony-i-smart-chasy-15501/'
sorting = 'sorting=rating'
number_required = 100
pattern = 'widget-search-result-container'
target = 'Смартфон'


def get_page(start_url: str):
    try:
        driver = make_driver()
        driver.get(start_url)
        sleep(round(random.uniform(2.1, 2.5), 2))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        html = driver.page_source
        with open('smart.html', 'w', encoding='utf-8') as f:
            f.write(html)
        '''if driver.find_element(By.CLASS_NAME, "aam4"):
            driver.execute_script(
                "return arguments[0].scrollIntoView(true);",
                WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CLASS_NAME, 'aam4')))
            )
        elif driver.find_element(By.CLASS_NAME, "aam7"):
            driver.execute_script(
                "return arguments[0].scrollIntoView(true);",
                WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CLASS_NAME, 'aam7')))
            )
        else:
            driver.execute_script(
                "return arguments[0].scrollIntoView(true);",
                WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CLASS_NAME, 'ma9a')))
            )
        html = driver.page_source'''
        return html
    except Exception as ex:
        print(ex)
    '''finally:
        driver.close()
        driver.quit()'''


def link_collector(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    if soup.find('div', attrs={'class', 'r3k'}):
        items = soup.find('div', attrs={'class', 'r3k'}).find_all('a')
    elif soup.find('div', attrs={'class': 'r9k'}):
        items = soup.find('div', attrs={'class', 'r9k'}).find_all('a')
    else:
        items = soup.find('div', attrs={'class', 'k5u'}).find_all('a')
    for item in items:
        links.append(item.get('href').split('?')[0])
    return set(links)


def get_smartphone_list():
    try:
        with open('smartfon_links.txt') as inf:
            list_of_smartphones = inf.read().splitlines()
    except FileNotFoundError:
        try:
            list_of_smartphones = []
            i = 1
            while len(list_of_smartphones) < 100:
                if i == 1:
                    category = '/category/telefony-i-smart-chasy-15501/'
                    url_param = '?sorting=rating'
                    html = get_page(start_url=url+category+url_param)
                else:
                    category = '/category/telefony-i-smart-chasy-15501/'
                    url_param = f'?page={str(i)}&sorting=rating'
                    html = get_page(start_url=url+category+url_param)
                links = link_collector(html)
                for link in links:
                    if 'product/smartfon' in link:
                        list_of_smartphones.append(link)
                print('Ищу смартфоны')
                print(f'Спарсил:{i} страниц')
                i += 1
                print(f'Смартфонов найдено {len(list_of_smartphones)}')
                sleep(round(random.uniform(2.1, 2.5), 2))

            with open('smartfon_links.txt', 'w', encoding='utf-8') as f:
                for link in list_of_smartphones:
                    f.write(link + '\n')
            print(f'Нашел {len(list_of_smartphones)} смартфонов')
            return list_of_smartphones

        except Exception as ex:
            print(ex)
    else:
        return list_of_smartphones


def get_data(some_list: list):
    try:
        with open('data.json', 'r') as inf:
            data = json.load(inf)
    except FileNotFoundError:
        data = {}
        i = 0
        try:
            for link in some_list:
                print('Парсим данные смартфонов')
                driver = make_driver()
                driver.get(f'{url+link}features/')
                html = driver.page_source
                with open('soup.html', 'w', encoding='utf-8') as f:
                    f.write(html)
                sleep(round(random.uniform(2.1, 2.5), 2))
                soup = BeautifulSoup(html, 'html.parser')
                items = []
                if soup.select_one(".d1.c3 .l5r"):
                    print('soup.select_one(".d1.c3 .l5r")')
                    items = soup.find_all('dd', attrs={'class', 'ly9'})
                else:
                    print('soup.select_one(".d1.c3 .q2l")')
                    items = soup.find_all('dd', attrs={'class', 'xl6'})
                for item in items:
                    os = item.get_text()
                    if 'iOS' in os or 'Android' in os:
                        print(os)
                        if os not in data.keys():
                            data.update({f'{os}': 1})
                        else:
                            data[os] += 1
                        print(data)
                i += 1
                print(f'Проверил {i} смартфон')
            with open('data.json', 'w') as ouf:
                json.dump(data, ouf)
            return data
        except Exception as ex:
            print(ex)
    else:
        return data


def make_dataframe(dictionary: dict):
    try:
        df = pd.read_csv('os_data.csv')
    except FileNotFoundError:
        def get_dict_wo_key(dictionary, key):
            _dict = dictionary.copy()
            _dict.pop(key, None)
            return _dict
        try:
            new_dict = get_dict_wo_key(dictionary, 'iOS')
        except KeyError as ex:
            print("No such key: '%s'" % ex.message)
        try:
            clean_dict = get_dict_wo_key(new_dict, 'Android')
        except KeyError as ex:
            print("No such key: '%s'" % ex.message)
        df = pd.DataFrame.from_dict(clean_dict, orient='index', index=clean_dict.keys(), columns=['Количество'])
        df.to_csv('os_data.csv')
        df = df.sort_values(by=['Количество'], ascending=False).copy()
        return df
    else:
        print(df.info)
        return df


def make_vis(dataframe):
    df = dataframe
    plt.figure()
    df.plot(kind='bar', xlabel='Версия ОС')
    plt.show()

def main():
    list_of_urls = get_smartphone_list()
    os_data = get_data(list_of_urls)
    dataframe = make_dataframe(os_data)
    make_vis(dataframe)



if __name__ == "__main__":
    main()
