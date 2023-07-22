from bs4 import BeautifulSoup
import requests
from loguru import logger

from results.group_info_parser import parse_group_info
from results.group_results_parser import parse_group_results


TITLE_INDEX = 0

# Загружаем страницу
url = 'http://o-mephi.net/cup/prot/Mosleto2023_x_spl.htm'
response = requests.get(url)

# Создаем объект BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Находим все заголовки h1 на странице
group_info_list = soup.find_all('h2')
group_result_list = soup.find_all('pre')[:-1]

for gi, group_result in enumerate(group_result_list):
    group_info = parse_group_info(group_info_list[gi].text)
    logger.success(group_info.group_code)
    parse_group_results(group_result)

# Выводим текст всех заголовков h1
