import random
from time import sleep
from driver import make_driver


# Simple function to load page using webdriver from driver.py
# Function return html as string
# As option - page could be saved if such option is chosen. By default, page will not be saved
# If you want to save page just do (save = True)
# By default saved page got None name, but it could be changed by (name = 'put your name here')
# File extension will be .html
def get_page(url: str, name: str = None, save=False):
    try:
        driver = make_driver()  # function from driver.py
        driver.get(url)
        sleep(round(random.uniform(1.5, 2.5), 2))  # to avoid ban
        # in case if page not static scroll page down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        html = driver.page_source
        if save:
            with open(f'{name}.html', 'w', encoding='utf-8') as f:
                f.write(html)
    except Exception as ex:
        print(ex)
        print(f'Error in {get_page.__name__} function')
    finally:
        driver.close()
        driver.quit()
        return html
