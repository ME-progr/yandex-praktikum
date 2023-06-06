import json

from logs import logs
from storages_research.config.settings import (
    test_settings,

    mongo_settings,
)
from storages_research.storages.context_managers import mongo_context

from storages_research.storages.mongo import MongoStorage
from storages_research.storages_tests.storages_tests import (
    StorageAverageInsertChunkDataTest,
    StorageAverageSelectDataTest,
)
from storages_research.storages_tests.utils import (
    get_mongo_id_pair,
)

logger = logs.get_file_logger()

if __name__ == "__main__":
    with (mongo_context(mongo_settings.host1, mongo_settings.host2) as mongo_client):
        storage = MongoStorage(mongo_client)
        # Тестирование среднего времени записи в таблциу по чанкам.
        chunk_sizes = (1, 20, 500, 1000)
        for chunk_size in chunk_sizes:
            StorageAverageInsertChunkDataTest(
                storage, count_tests=test_settings.tests_count, chunk_size=chunk_size
            ).execute()

        # Тестирование среднего времени получения количества записей в таблице.
        StorageAverageSelectDataTest(
            storage,
            count_tests=test_settings.tests_count,
            query=None,
            label="select_count",
        ).execute()
        ids = get_mongo_id_pair(storage)
        # Тестирование среднего времени получения фильмов для пары film_id, user_id.
        StorageAverageSelectDataTest(
            storage,
            count_tests=test_settings.tests_count,
            query=json.dumps(ids),
            label="select_user_films",
        ).execute()
