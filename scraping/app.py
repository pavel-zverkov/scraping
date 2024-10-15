from .mos_season_results.web_parser.results_parser import ResultsParser
from .mos_season_results.web_transformer.results_api_transfmormer import ResultsAPITransformer
from .mos_season_results.uploader.result_uploader import ResultUploader

from .logger import logger

URL = 'http://o-mephi.net/cup/prot/Mosleto2024_12_spl.htm'
# URL = 'http://o-mephi.net/cup/prot/Den_Pobedi_2024_spl.htm'


@logger.catch
def main() -> None:
    parser = ResultsParser(URL)
    transformer = ResultsAPITransformer()
    uploader = ResultUploader(URL)

    results = parser.parse()
    results = transformer.transform_results(results)
    uploader.upload(results)

    logger.success(URL)


if __name__ == '__main__':
    # for i in range(1, 11):
    #     URL = f'http://o-mephi.net/cup/prot/Mosleto2024_{i}_spl.htm'
    #     main()
    main()
