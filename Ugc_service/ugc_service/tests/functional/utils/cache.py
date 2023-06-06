from hashlib import sha256


def make_cache_id_by_template(class_name: str, func_name: str, *args, **kwargs) -> str:
    """
    Метод генерирует ключ кэша по переданным параметрам.

    Args:
        class_name: наименование класса
        func_name: наименование функции
        args: позиционные аргументы
        kwargs: именованные аргументы

    Returns:
        cache_id
    """
    datas = f'{class_name}_{func_name}_{args}_{kwargs}'
    cache_id = sha256(datas.encode('utf-8')).hexdigest()
    return cache_id
