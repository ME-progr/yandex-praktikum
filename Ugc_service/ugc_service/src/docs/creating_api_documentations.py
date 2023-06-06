"""Модуль инициализации документации Swagger."""

from os import path

from ugc_service.src.api.v1.events import write_film_frame
from ugc_service.src.api.v1.film_rating import (
    set_film_user_rating, get_film_user_rating, update_film_user_rating,
    delete_film_user_rating, get_average_film_rating
)
from ugc_service.src.api.v1.film_review import (
    create_film_user_review, get_film_user_review, update_film_user_review,
    delete_film_user_review, get_film_reviews
)
from ugc_service.src.api.v1.user_bookmark import (
    add_film_to_user_bookmarks, delete_film_from_user_bookmarks, get_user_bookmarks
)


def convert_docstring_to_swagger_description(docstring: str) -> str:
    """функция преобразует документ-строку функции в описание для Swagger."""
    docstring = docstring[1:-2]
    result = []
    for row in docstring.split('\n'):
        if 'service' not in row and 'credentials' not in row:
            result.append(row)

    return '<br>'.join(result).replace('    ', '&emsp;')


def write_documentations_to_file():
    with open('api_documentations.py', 'w', encoding='utf-8') as file:
        file.write('"""\nМодуль объектов документации swagger.\n'
                   f'Создано автоматически модулем `{path.basename(__file__)}`\n"""\n\n')

        api_endpoints = [
            write_film_frame, set_film_user_rating, get_film_user_rating, update_film_user_rating,
            delete_film_user_rating, get_average_film_rating, create_film_user_review, get_film_user_review,
            update_film_user_review, delete_film_user_review, get_film_reviews, add_film_to_user_bookmarks,
            delete_film_from_user_bookmarks, get_user_bookmarks
        ]
        api_endpoint_description_names = [f'{func.__name__.upper()}_DESCRIPTION' for func in api_endpoints]

        for api_endpoint, description_name in zip(api_endpoints, api_endpoint_description_names):
            docstring = convert_docstring_to_swagger_description(api_endpoint.__doc__)
            file.write(f'{description_name} = """{docstring}"""\n')


if __name__ == '__main__':
    write_documentations_to_file()
