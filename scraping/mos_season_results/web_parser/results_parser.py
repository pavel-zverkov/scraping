import locale

import requests
from bs4 import BeautifulSoup

from ...parser.parser_entity import Parser
from .. import constants as c
from ..errors.parser_errors import GroupCountError
from .competition_results import CompetitionResults, GroupResults
from .utils import parse_group_info, parse_group_results

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class ResultsParser(Parser):

    def parse(self) -> CompetitionResults:
        super().parse()

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        title_info = soup.find('h1').text
        group_info_list = soup.find_all('h2')
        group_result_list = soup.find_all('pre')[:c.FOOTPRINT_INDEX]

        if len(group_info_list) != len(group_result_list):
            raise GroupCountError(
                'Quantity of group titles and results not equal')

        competition_results: list[GroupResults] = []
        for group_info, group_result in zip(group_info_list, group_result_list):
            ctrl_points_order, result_list = parse_group_results(group_result)
            info = parse_group_info(group_info, ctrl_points_order)

            competition_results.append(GroupResults(info, result_list))

        return CompetitionResults(title_info, competition_results)


if __name__ == '__main__':
    MOS_SEASON_URL = 'http://o-mephi.net/cup/prot/Mosleto2023_9_spl.htm'
    result_parser = ResultsParser(MOS_SEASON_URL)
    result_parser.parse()
