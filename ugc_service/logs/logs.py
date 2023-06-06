"""Модуль предназначен для реализации формирования логгера для других модулей."""

import logging
import sys
from functools import lru_cache
from logging.handlers import RotatingFileHandler

from logs.settings import (
    BASE_FORMAT, BASE_LOG_LEVEL, BASE_LOGGER_NAME,
    BASE_PATH_FOR_LOG_FILE, BASE_LOG_FILE_BYTE_SIZE,
    BASE_BACKUP_COUNT,
)


@lru_cache()
def get_stream_logger() -> logging.Logger:
    """
    Функция формирует логгер для заданного пространства имен.

    Returns:
        Logger
    """
    logger = logging.getLogger(BASE_LOGGER_NAME)
    logger.setLevel(BASE_LOG_LEVEL)
    logger_handler = logging.StreamHandler(sys.stdout)
    logger_formatter = logging.Formatter(BASE_FORMAT)
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)

    return logger


@lru_cache()
def get_file_logger(logs_file_path: str = BASE_PATH_FOR_LOG_FILE, mode: str = 'a') -> logging.Logger:
    """
    Функция формирует логгер для заданного пространства имен.

    Args:
        logs_file_path: Путь до файла логов.
        mode: мод работы с файлом, по умолчанию 'a'
    Returns:
        Logger
    """
    logger = logging.getLogger(BASE_LOGGER_NAME)
    logger.setLevel(BASE_LOG_LEVEL)
    logger_handler = RotatingFileHandler(
        logs_file_path,
        encoding='utf-8',
        maxBytes=BASE_LOG_FILE_BYTE_SIZE,
        backupCount=BASE_BACKUP_COUNT,
        mode=mode
    )
    logger_formatter = logging.Formatter(BASE_FORMAT)
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)

    return logger
