"""
Логгер проекта
"""
from loguru import logger
from sys import stdout

FMT = ('{time:HH:mm:ss} <level>{level: <8}</level>' +
       '<cyan>{name}:{function}:{line}</cyan> ' +
       '- <level>{message}</level>')


# delete default logger and set new logger
logger.remove()
logger.add(
    sink=stdout,
    colorize=True,
    format=FMT, level='DEBUG'
)
