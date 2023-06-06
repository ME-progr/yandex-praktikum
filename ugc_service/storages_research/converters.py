"""Модуль содержит конвертеры для полей."""
from iso8601 import iso8601

FILM_VIEW_CONVERTER = dict(
    user_id=str,
    film_id=str,
    film_frame=int,
    created_at=iso8601.parse_date,
)

FILM_RATING_CONVERTER = dict(
    user_id=str,
    film_id=str,
    rating=int,
)
