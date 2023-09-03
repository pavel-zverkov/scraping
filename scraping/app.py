from .mos_season_results.web_parser.results_parser import ResultsParser
from .mos_season_results.web_transformer.results_api_transfmormer import ResultsAPITransformer
from .mos_season_results.uploader.result_uploader import ResultUploader

from .logger import logger

URL = 'http://o-mephi.net/cup/prot/Mosleto2023_9_spl.htm'


@logger.catch
def main() -> None:
    parser = ResultsParser(URL)
    transformer = ResultsAPITransformer()
    uploader = ResultUploader()

    results = parser.parse()
    results = transformer.transform_results(results)
    uploader.upload(results)


if __name__ == '__main__':
    main()
