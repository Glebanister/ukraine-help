import enum
import logging

from typing import Dict


class LogLevel(enum.Enum):
    ERROR = 0
    INFO = 1
    DEBUG = 2


LOGGERS: Dict[str, logging.Logger] = {}


def get_logger(actor: str) -> logging.Logger:
    if actor not in LOGGERS:
        LOGGERS[actor] = logging.getLogger(actor)
    return LOGGERS[actor]


def log(level: LogLevel, actor: str, msg: str) -> None:
    if level == LogLevel.ERROR:
        get_logger(actor).log(logging.ERROR, msg)
    elif level == LogLevel.INFO:
        get_logger(actor).log(logging.INFO, msg)
    elif level == LogLevel.DEBUG:
        get_logger(actor).log(logging.DEBUG, msg)


def log_error(actor: str, msg: str) -> None:
    log(LogLevel.ERROR, actor, msg)


def log_info(actor: str, msg: str) -> None:
    log(LogLevel.ERROR, actor, msg)


def log_debug(actor: str, msg: str) -> None:
    log(LogLevel.ERROR, actor, msg)
