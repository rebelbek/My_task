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
data = None
stocks_list = []

for i in soup.find_all('data'):
    if i['id'] == 'securities':
        data = i
        break

rows = data.select('row')

for row in rows:
    tmp_dict = {} #для временного хранения значений из одной строки row
    for item in list_names:
        tmp_dict[item] = row[item.upper()]
    stocks_list.append(tmp_dict)

for item in stocks_list:
    tmp_list = []
    for key, value in item.items():
        tmp_list.append(f'{key.title()} = {value}')
    print(' | '.join(tmp_list))
    print('-' * 130)


