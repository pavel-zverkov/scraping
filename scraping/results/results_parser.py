from datetime import date, datetime
from typing import NamedTuple
from parser.parser_entity import Parser

import requests
from bs4 import BeautifulSoup
from results.group_info_parse_utils import parse_group_info
from results.group_results_entity import GroupResultsEntity
from results.group_results_parse_utils import parse_group_results
from results.results_constants import FOOTPRINT_INDEX
from results.results_parser_errors import GroupCountError

from logger import logger
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class ResultEntity(NamedTuple):
    event_name: str
    competition_name: str
    competition_date: date
    control_points: list[int]
    class_list: list[str]
    competition_result: list[GroupResultsEntity]


class ResultsParser(Parser):

    def parse(self) -> list[ResultEntity]:
        super().parse()

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        title_info_list = [item.strip()
                           for item in soup.find('h1').text.split('\n')]

        event_name = title_info_list[2]
        competition_name = title_info_list[3]
        competition_date = datetime.strptime(
            title_info_list[4].split(',')[0], '%d %B %Y')

        group_info_list = soup.find_all('h2')
        group_result_list = soup.find_all('pre')[:FOOTPRINT_INDEX]

        if len(group_info_list) != len(group_result_list):
            raise GroupCountError(
                'Quantity of group titles and results not equal')

        results: list[GroupResultsEntity] = []
        for group_info, group_result in zip(group_info_list, group_result_list):
            ctrl_points_order, result_list = parse_group_results(group_result)
            info = parse_group_info(group_info, ctrl_points_order)

            results.append(GroupResultsEntity(info, result_list))

        competition_dict: dict[str, list[GroupResultsEntity]] = {}
        for result in results:
            key = str(result.info.ctrl_points_order)
            value = result
            # logger.info(result.info)
            if key not in competition_dict.keys():
                competition_dict[key] = [value]
                # logger.debug('Create')
            else:
                competition_dict[key].append(value)
                # logger.debug('Append')
            # logger.debug(competition_dict)

        sorted_keys = sorted(competition_dict.keys(),
                             key=lambda x: len(x), reverse=True)
        competition_dict = dict(
            zip(sorted_keys, [competition_dict[key] for key in sorted_keys]))

        # logger.info(competition_dict)
        output = []
        for key, value in competition_dict.items():
            output.append(
                ResultEntity(
                    event_name=event_name,
                    competition_name=competition_name,
                    competition_date=competition_date.date(),
                    control_points=str_to_int_list(key),
                    class_list=[
                        (item.info.gender.value +
                         str(item.info.age) + item.info.additional_code)
                        for item in value
                    ],
                    competition_result=value
                )
            )

        return output


def str_to_int_list(s: str) -> list[str]:
    return s.replace('[', '').replace(']', '').split(', ')
