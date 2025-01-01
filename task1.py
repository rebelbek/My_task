import os
import requests
from dotenv import dotenv_values, load_dotenv
from bs4 import BeautifulSoup #внешний модуль
#Дополнительно должен быть установлен модуль lxml(он нужен для BeautifulSoup)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
moex_api_url = os.environ.get('url')

response = requests.get(moex_api_url)
soup = BeautifulSoup(response.content, 'xml')
list_names = ['secid', 'boardid', 'shortname', 'lotsize', 'secname', 'listlevel', 'issuesize']


def get_rows():
    data = None
    for i in soup.find_all('data'):
        if i['id'] == 'securities':
            data = i
            break
    rows = data.select('row')
    return rows


def get_stocks_list():
    rows = get_rows()
    stocks_list = []
    for row in rows:
        tmp_dict = {} #для временного хранения значений из одной строки row
        for item in list_names:
            if row[item.upper()].isdigit():
                tmp_dict[item] = int(row[item.upper()])
            else:
                tmp_dict[item] = row[item.upper()]
        stocks_list.append(tmp_dict)
    return stocks_list


def show_stocks_list():
    stocks_list = get_stocks_list()
    for item in stocks_list:
        tmp_list = []
        for key, value in item.items():
            tmp_list.append(f'{key.title()} = {value}')
        print(' | '.join(tmp_list))
        print('-' * 130)

if __name__ == "__main__":
    show_stocks_list()


