from abc import abstractmethod
from parser.parser_output_entity import ParserOutputEntity


class Parser:
    def __init__(
        self,
        url: str
    ) -> None:
        
        self.url = url

    @abstractmethod
    def parse(self) -> ParserOutputEntity:
        pass