"""
Вспомогательные функции для преобразования документации функций в описание для Swagger,
используя синтаксис Markdown.
"""


def convert_docstring_to_swagger_description(docstrings: list) -> list:
    """функция преобразует документ-строку функции в описание для Swagger."""

    result = []
    for docstring in docstrings:
        docstring = docstring[1:]
        result.append(docstring.replace('    ', '&emsp;').replace('\n', '<br>'))
    return result


def get_docstrings_from_file(file_name: str):
    """Функция для взятия документ-строк из файла."""

    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read()
    def_count = data.count('def ')
    data = data.split('"""')
    data = data[-2:0:-2][:def_count]
    return data


def get_description_for_swagger(file_name: str) -> list:
    """Функция взятия и преобразования описания для Swagger."""

    data = get_docstrings_from_file(file_name)
    return convert_docstring_to_swagger_description(data)
