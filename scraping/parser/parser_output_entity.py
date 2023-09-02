from typing import Any, NamedTuple

from .parser_output_enum import OutputStatus


class ParserOutputEntity(NamedTuple):
    status_code: OutputStatus
    error_message: str
    data: Any