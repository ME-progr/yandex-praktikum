"""Модуль создания тестовых данных."""

import csv
from datetime import datetime
from uuid import uuid4
import random


def generate_csv_film_view_data(rows_count: int, mongo: bool = False):
    """
    Функция, записывающая тестовые данные в файл `test_data.csv`.

    Args:
        rows_count (int): количество строк.
        mongo (bool): генерировать для монго
    """

    with open("film_view_data.csv", "w") as file:
        writer = csv.writer(file, delimiter=",")
        if not mongo:
            writer.writerow(("user_id", "film_id", "film_frame", "created_at"))
        else:
            writer.writerow(("user_id", "film_id", "rating"))
        writer.writerows(iter_random_film_view(rows_count, mongo=mongo))


def iter_random_film_view(rows_count: int, mongo: bool = False):
    """
    Функция, создающая тестовые данные.

    Args:
        rows_count (int): количество строк.
        mongo (bool): генерировать для монго
    Yields:
        генератор.
    """
    for row in range(rows_count):
        if not mongo:
            yield (
                str(uuid4()),
                str(uuid4()),
                random.getrandbits(50),
                datetime.now(),
            )
        else:
            yield {
                "film_id": str(uuid4()),
                "user_id": str(uuid4()),
                "rating": random.randint(1, 10),
            }


def iter_csv(file_path: str, converters: dict):
    """
    Функция возвращает сконвертированный файл csv  в виде генератора.

    Args:
         file_path: путь до файла csv
         converters: название поля и функция, которая конвертирует его к заданному типу.
    """
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            yield {
                k: (converters[k](v) if k in converters else v) for k, v in line.items()
            }
