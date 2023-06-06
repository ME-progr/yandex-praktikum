"""Модуль отвечает за собственные исключения для работы с кэшем."""


class MissCacheInterfaceRealisation(Exception):
    """Исключение выбрасывается в том случае, если для заданного клиента кэша нет реализации интерфейса."""

    def __init__(self, client, message='Для заданного клиента кэша нет реализованного интерфейса.'):
        self.client_type = type(client)
        self.message = message
        super().__init__(self.message)


class MissCacheClientInClass(Exception):
    """Исключение выбрасывается в том случае, если в классе не задан атрибут self.cache_client."""

    def __init__(self, class_name: str, message='В классе не задан атрибут self.cache_client.'):
        self.class_name = class_name
        self.message = f'{message}: {self.class_name}'
        super().__init__(self.message)
