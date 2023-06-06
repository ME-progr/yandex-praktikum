import os
from logs import logs
from storages_research.config.settings import (
    clickhouse_settings, vertica_connection_info,
    test_settings, BASE_DIR
)
from storages_research.converters import FILM_VIEW_CONVERTER
from storages_research.storages.context_managers import clickhouse_context
from storages_research.storages.factories import get_storage_by_client, get_manager_by_client
from storages_research.storages_tests.storages_tests import (
    StorageInsertCsvTest, StorageAverageInsertChunkDataTest, StorageAverageSelectDataTest,
)
from storages_research.storages_tests.utils import get_user_id_from_storage, get_film_id_from_storage
from storages_research.storages_tests.storages_select import SelectQuery, get_select_query_by_client

import vertica_python

logger = logs.get_file_logger()

if __name__ == '__main__':
    film_view_csv = os.path.join(BASE_DIR, 'storages_research', 'film_view_data.csv')

    if not os.path.isfile(film_view_csv):
        raise FileNotFoundError(
            "Файл film_view_data.csv не найден. Создайте тестовые данные с помощью generate_csv_data.py"
        )

    with (
        clickhouse_context(clickhouse_settings.host, clickhouse_settings.port) as clickhouse_client,
        vertica_python.connect(**vertica_connection_info) as vertica_client
    ):

        clients = (clickhouse_client, vertica_client,)

        for client in clients:
            manager = get_manager_by_client(client)
            storage = get_storage_by_client(client)

            manager.on_start_up()

            # Тестирование времени вставки больших данных из csv.
            StorageInsertCsvTest(storage).execute(
                target='ugc.film_view',
                file_path=film_view_csv,
                converters=FILM_VIEW_CONVERTER
            )

            user_id = get_user_id_from_storage(storage)
            film_id = get_film_id_from_storage(storage)

            # Тестирование среднего времени получения количества записей в таблице.
            query = get_select_query_by_client(client, SelectQuery.COUNT)
            StorageAverageSelectDataTest(
                storage,
                count_tests=test_settings.tests_count,
                query=query,
                label='select_count',
            ).execute()

            # Тестирование среднего времени получения фильмов для конкретного пользователя.
            query = get_select_query_by_client(client, SelectQuery.USER_FILMS).format(user_id=f"'{user_id}'")
            StorageAverageSelectDataTest(
                storage,
                count_tests=test_settings.tests_count,
                query=query,
                label='select_user_films',
            ).execute()

            # Тестирование среднего времени получения пользователей для конкретного фильма.
            query = get_select_query_by_client(client, SelectQuery.FILM_USERS).format(film_id=f"'{film_id}'")
            StorageAverageSelectDataTest(
                storage,
                count_tests=test_settings.tests_count,
                query=query,
                label='select_film_users',
            ).execute()

            # Тестирование среднего времени записи в таблциу по чанкам.
            chunk_sizes = (1, 20, 500, 1000)
            for chunk_size in chunk_sizes:
                StorageAverageInsertChunkDataTest(storage, count_tests=test_settings.tests_count, chunk_size=chunk_size).execute()

            manager.on_shut_down()
