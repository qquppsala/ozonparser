from list_constructor import make_list
from dict_constructor import make_json
from df_constructor import check_dataframe
from visualization import make_bar

url = 'https://www.ozon.ru'
category = '/category/telefony-i-smart-chasy-15501/'  # категория товаров
sorting = 'sorting=rating'  # сортировка "Высокий рейтинг"
number_required = 14  # Первые 100 смартфонов
pattern = 'widget-search-result-container'  # тэг для парсинга
target_for_product = 'Смартфон'  # таргет для парсинга
target_for_data = 'Версия'  # таргет для парсинга
name_for_list = 'spisok_smartov'  # имя для списка ссылок на смартфоны
name_for_dict = 'os_data'  # имя для словаря с данными


def main():
    # Парсим озон в категории товаров "Телефоны и смарт-часы" с сортировкой "Высокий рейтинг"
    # создаем список из первых 100 ссылок на смартфоны
    list_of_smartphones_urls = make_list(
        name=name_for_list,
        url=url,
        category=category,
        sorting=sorting,
        number_required=number_required,
        pattern=pattern,
        target=target_for_product
    )

    # Парсим версию ОС в каждой ссылке из листа, и записываем в словарь
    # Вид словаря {"Версия ОС" : "Сколько раз встречается"}
    smartphones_os_data = make_json(
        some_list=list_of_smartphones_urls,
        url=url,
        name=name_for_dict,
        target=target_for_data
    )

    # Из словаря создаем датафрейм и смотрим распределение
    df = check_dataframe(name=name_for_dict, dictionary=smartphones_os_data)
    make_bar(dataframe=df)


if __name__ == "__main__":
    main()
