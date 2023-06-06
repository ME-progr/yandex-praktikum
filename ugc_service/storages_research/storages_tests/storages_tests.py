import os
import time
from abc import ABC

from storages_research.config import settings
from storages_research.config.settings import BASE_DIR
from storages_research.storages.interfaces import Storage
from storages_research.storages.mongo import MongoStorage
from storages_research.utils import iter_random_film_view
from storages_research.storages_tests.storages_plots import create_test_plot

from logs import logs

RESEARCH_RESULTS_LOGS = os.path.join(
    BASE_DIR, 'storages_research', 'research_results', 'tests.logs'
)
PLOTS_PATH = os.path.join(BASE_DIR, 'storages_research', 'research_results')

logger = logs.get_file_logger(RESEARCH_RESULTS_LOGS, mode="w")


class StorageTest(ABC):
    """Класс предоставляет возможность протестировать функционал хранилищ на скорость."""

    name = "default_test"

    def __init__(self, storage, *_, write_logs: bool = True):
        self._storage = storage
        self._write_logs = write_logs

    def execute(self, *args, **kwargs):
        start_time = time.time()
        self._storage_action(*args, **kwargs)
        delta_time = time.time() - start_time
        self._log(
            f'Хранилище: {self._storage.name}. Тест: {self.name}. Время выполнения: {delta_time} секунд.'
        )
        return delta_time

    def _log(self, msg: str):
        if self._write_logs:
            logger.info(msg)

    def _storage_action(self, *args, **kwargs):
        """Метод должен реализовывать какое-то действие с хранилищем, которое будем тестировать на скорость."""
        pass


class StorageAverageTestMixin:
    """Класс-миксин позволяет определить среднее время выполнения определенного теста."""

    def __init__(self):
        self._test_for_average: StorageTest = None
        self._tests_params = []
        self._plot_path: str = ""
        self._plot_title: str = ""

    def _execute_average(self):
        """Метод вычисляет среднее время выполнения и строит график."""
        execution_time = []
        for params in self._tests_params:
            execution_time.append(self._test_for_average.execute(**params))

        average_time = sum(execution_time) / len(execution_time)
        create_test_plot(
            file_path=self._plot_path,
            x=range(len(execution_time)),
            y=execution_time,
            title=self._plot_title,
        )
        return average_time


class StorageInsertCsvTest(StorageTest):
    """Запись в хранилище из csv файла"""

    name = "Запись в хранилище из CSV файла"

    def _storage_action(self, *args, **kwargs):
        self._storage.import_from_csv(*args, **kwargs)


class StorageInsertChunkDataTest(StorageTest):
    """Тестирование записи в хранилище пачки данных"""

    name = "Запись в хранилище пачки данных"

    def _storage_action(self, *args, **kwargs):
        self._storage.write_data(*args, **kwargs)


class StorageAverageInsertChunkDataTest(StorageTest, StorageAverageTestMixin):
    """Тестирование среднего времени вставки пачки данных в хранилище"""

    name = "Среднее время записи в хранилище пачки данных"

    def __init__(
        self,
        storage: Storage | MongoStorage,
        count_tests: int,
        chunk_size: int,
        *_,
        write_logs: bool = True,
    ):
        StorageTest.__init__(self, storage, write_logs=write_logs)
        StorageAverageTestMixin.__init__(self)

        self._test_for_average = StorageInsertChunkDataTest(storage, write_logs=False)
        self._chunk_size = chunk_size
        self._plot_path = os.path.join(
            PLOTS_PATH,
            f'{self._storage.name}_{self._chunk_size}_average_chunk_insert.png',
        )
        self._plot_title = f'Скорость записи пачки размером {chunk_size}'

        for _ in range(count_tests):
            self._tests_params.append(
                dict(target="", data=iter_random_film_view(chunk_size, mongo=settings.mongo_settings.mongo_test))
            )

    def execute(self, *args, **kwargs):
        average_time = self._execute_average()
        self._log(
            f'Хранилище: {self._storage.name}. Тест: {self.name}. Размер пачки: {self._chunk_size}. '
            f'Количество тестов: {len(self._tests_params)}. Среднее время выполнения: {average_time} секунд.'
        )
        return average_time


class StorageSelectDataTest(StorageTest):
    """Тестирование времени считывания данных из хранилища."""

    name = "Считывание данных из хранилища"

    def _storage_action(self, *args, **kwargs):
        self._storage.get_data(*args, **kwargs)


class StorageAverageSelectDataTest(StorageTest, StorageAverageTestMixin):
    """Тестирование среднего времени считывания данных из хранилища."""

    name = "Среднее время считывания данных из хранилища"

    def __init__(
        self,
        storage: Storage | MongoStorage,
        count_tests: int,
        query: str | None,
        *_,
        write_logs: bool = True,
        label: str = "",
    ):
        StorageTest.__init__(self, storage, write_logs=write_logs)
        StorageAverageTestMixin.__init__(self)

        self._test_name = label or self.name
        self._test_for_average = StorageSelectDataTest(storage, write_logs=False)
        self._plot_path = os.path.join(
            PLOTS_PATH, f'{self._storage.name}_{self._test_name}_average_select.png'
        )
        self._plot_title = 'Скорость считывания данных'

        for _ in range(count_tests):
            self._tests_params.append(dict(query=query))

    def execute(self, *args, **kwargs):
        average_time = self._execute_average()
        self._log(
            f'Хранилище: {self._storage.name}. Тест: {self._test_name}. '
            f'Количество тестов: {len(self._tests_params)}. Среднее время выполнения: {average_time} секунд.'
        )
        return average_time
