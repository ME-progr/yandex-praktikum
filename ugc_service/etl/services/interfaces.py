"""Модуль с интерфейсами."""

from abc import abstractmethod, ABC


class BaseBrokerExtractor(ABC):
    """Базовый класс, отвечающий за выгрузку данных."""

    def __init__(self, consumer):
        self._consumer = consumer

    @abstractmethod
    def extract(self, *args):
        """Метод вытаскивает данные."""
        pass


class BaseDatabaseLoader(ABC):
    """Базовый класс, отвечающий за загрузку данных."""

    def __init__(self, client):
        self._client = client

    @abstractmethod
    def load(self, *args, **kwargs) -> None:
        """Метод сохраняет записи в базу."""
        pass


class BaseExtractorAdapter(ABC):
    """Базовый класс, отвечающий за адаптирование данных."""

    @abstractmethod
    def adapt(self, value):
        """Метод адаптирует полученные данные."""
        pass
