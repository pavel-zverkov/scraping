from json import dumps
from requests import post
from competition.competition_entity import Competition
from logger import logger
from results.result_person_searcher import ResultPersonSearcher
from results.results_parser import ResultsParser
from splits.split_comparer import SplitComparer
from splits.split_entity import Split

URL = 'http://o-mephi.net/cup/prot/Mosleto2023_15_spl.htm'
PERSON_1 = 'Ольховский Дмитрий'
PERSON_2 = 'Хамурзов Владимир'

SPLIT_API_URL = 'http://localhost:8000/'


@logger.catch
def main() -> None:
    results_parser = ResultsParser(URL)
    competition_result_list = results_parser.parse()

    for i, competition_result in enumerate(competition_result_list):
        competition_data = {
            'name': f'D{i + 1}',
            'date': competition_result.competition_date.strftime('%Y-%m-%d'),
            'class_list': competition_result.class_list,
            'control_point_list': competition_result.control_points,
            'kind': 'orient',
            'format': 'кросс-классика'
        }
        logger.info(competition_data)
        post(SPLIT_API_URL + 'competition/', json=competition_data)

    # searcher = ResultPersonSearcher(results)
    # split_1 = searcher.search(PERSON_1)
    # split_2 = searcher.search(PERSON_2)

    # comparer = SplitComparer()
    # comparer.display_compare(split_1, split_2)


if __name__ == '__main__':
    main()
    # PURPLE = '\033[95m'
    # CYAN = '\033[96m'
    # DARKCYAN = '\033[36m'
    # BLUE = '\033[94m'
    # GREEN = '\033[92m'
    # YELLOW = '\033[93m'
    # RED = '\033[91m'
    # BOLD = '\033[1m'
    # UNDERLINE = '\033[4m'
    # END = '\033[0m'
    # t = RED + 'hello, world'
    # print(f'{t:>40}{END}')
    # print(len(t))
