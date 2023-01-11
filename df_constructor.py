import pandas as pd


# Simple function to check whether dataframe is already exist as file with given name
# in same folder with parser
# File should have .csv extension. And name should be given without extension
# If file with given name not exist function will call make_dataframe() to create one
# Function saves dataframe by default, if you don't need one just do (save = False)
# Function returns dataframe as pandas dataframe object
# Because parser was used for ozon.ru some tuning was done on called functions
def check_dataframe(name: str, dictionary: dict):
    try:
        print(f'Ищу {name}.csv')
        df = pd.read_csv(f'{name}.csv', index_col=0)
    except FileNotFoundError:
        print('Файл не найден')
        print(f'Создаю новый {name}.csv')
        df = make_dataframe(dictionary, name)
        return df
    else:
        print('Файл найден')
        print('Результат', '\n', df, '\n', "*"*30)
        return df

# Function to clean data if needed
# Not used
#def get_dict_wo_key(dictionary: dict, key: str):
#            _dict = dictionary.copy()
#            _dict.pop(key, None)
#            return _dict


# Simple function to make dataframe from given dictionary
# Function will save dataframe as .csv in same folder with parser with given name in (name=)
# Function returns dataframe as pandas dataframe object
# Dataframe ascending=False
def make_dataframe(dictionary: dict, name: str = 'Dataframe', save=True):
    try:
        df = pd.DataFrame.from_dict(dictionary, orient='index', columns=['Количество'])
        df.sort_values(by=['Количество'], ascending=False, inplace=True)
        if save:
            df.to_csv(f'{name}.csv', header=True, index=True)
    except Exception as ex:
        print(ex)
        print(f'Error in {make_dataframe.__name__} function')
    else:
        print('Файл создан')
        print('Финальный результат', '\n', df, '\n', "*"*30)
        return df
