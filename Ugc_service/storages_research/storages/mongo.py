"""Модуль отвечает за хранилище Mongo."""
import json
from typing import Iterable, Generator

from pymongo import MongoClient
from pymongo.collection import Collection

from storages_research.storages.interfaces import Storage, StorageManager
from storages_research.utils import iter_csv


class MongoStorage:
    """Описывает работу с хранилищем Mongo"""

    name = "Mongo"

    def __init__(self, client: MongoClient):
        self.collection: Collection = client.ugc.film_rating

    def get_data(self, query=None):
        result = []
        if not query:
            for row in self.collection.find():
                result.append(row)
        else:
            for row in self.collection.find(json.loads(query)):
                result.append(row)
        return result

    def write_data(self, target: str, data: Iterable[dict]):
        self.collection.insert_many(data)
