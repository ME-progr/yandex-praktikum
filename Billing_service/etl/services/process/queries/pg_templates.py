"""Модуль содержит шаблоны SQL запросов для PostgreSQL."""

MOVIES_QUERY = """
    SELECT
        film_work.id,
        film_work.title,
        film_work.modified as modified_state
    FROM
        content.film_work film_work
    {where_condition}
    ORDER BY film_work.modified
"""


BILLING_QUERY = """
    SELECT
        fw.id,
        array_remove(array_agg(sb.subscribe_type), NULL) subscribe_types,
        fw.modified_subscribe_date modified_state
    FROM
        billing.filmwork fw
    LEFT JOIN
        billing.filmwork_subscribe fw_sb
    ON
        fw.id = fw_sb.filmwork_id
    LEFT JOIN
        billing.subscribe sb
    ON
        sb.id = fw_sb.subscribe_id
    {where_condition}
    GROUP BY
        fw.id, fw.modified_subscribe_date
    ORDER BY
        fw.modified_subscribe_date
"""
