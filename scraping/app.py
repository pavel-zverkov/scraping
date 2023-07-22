from bs4 import BeautifulSoup
import requests
from loguru import logger


TITLE_INDEX = 0

# Загружаем страницу
url = 'http://o-mephi.net/cup/prot/Mosleto2023_12_spl.htm'
response = requests.get(url)

# Создаем объект BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Находим все заголовки h1 на странице
group_info_list = soup.find_all('h2')
group_result_list = soup.find_all('pre')[:-1]

for group_result in group_result_list:
    for i, item in enumerate(group_result):
        logger.info(item)
    break

# Выводим текст всех заголовков h1
