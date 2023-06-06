"""Модуль вспомогательных функций для Persons."""

from models.persons import Person, PersonRoles


def adapt_elastic_row_to_person(row: dict) -> Person:
    """Функция конвертирует ответ от Elasticsearch в модель Person."""
    row['roles'] = PersonRoles(
        actor=row.pop('actor', []),
        writer=row.pop('writer', []),
        director=row.pop('director', []),
        other=row.pop('other', [])
    )

    return Person(**row)
