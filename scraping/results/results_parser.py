from parser.parser_entity import Parser

import requests
from bs4 import BeautifulSoup
from results.group_info_parse_utils import parse_group_info
from results.group_results_entity import GroupResultsEntity
from results.group_results_parse_utils import parse_group_results
from results.results_constants import FOOTPRINT_INDEX
from results.results_parser_errors import GroupCountError


class ResultsParser(Parser):

    def parse(self) -> list[GroupResultsEntity]:
        super().parse()

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        group_info_list = soup.find_all('h2')
        group_result_list = soup.find_all('pre')[:FOOTPRINT_INDEX]

        if len(group_info_list) != len(group_result_list):
            raise GroupCountError(
                'Quantity of group titles and results not equal')

        results = []
        for group_info, group_result in zip(group_info_list, group_result_list):
            ctrl_points_order, result_list = parse_group_results(group_result)
            info = parse_group_info(group_info, ctrl_points_order)

            results.append(GroupResultsEntity(info, result_list))

        return results
