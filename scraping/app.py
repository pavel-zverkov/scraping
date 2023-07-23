from loguru import logger
from results.result_person_searcher import ResultPersonSearcher
from results.results_parser import ResultsParser

URL = 'http://o-mephi.net/cup/prot/Mosleto2023_7_spl.htm'
SEARCH_ENTITY = 'Хамурзова Мария'


@logger.catch
def main() -> None:
    results_parser = ResultsParser(URL)
    results = results_parser.parse()

    searcher = ResultPersonSearcher(SEARCH_ENTITY)

    logger.info(searcher.search(results))


if __name__ == '__main__':
    main()
