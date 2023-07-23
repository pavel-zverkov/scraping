from abc import abstractmethod
from typing import Any

# from parser.parser_output_entity import ParserOutputEntity


class Parser:
    def __init__(
        self,
        url: str
    ) -> None:

        self.url = url

    # TODO: переделать возвращаемый тип
    @abstractmethod
    def parse(self) -> Any:
        pass
