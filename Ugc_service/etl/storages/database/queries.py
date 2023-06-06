"""Модуль запрос в базу данных."""

CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS ugc.film_view
    ON CLUSTER company_cluster
        (
            user_id UUID,
            film_id UUID,
            film_frame Float64,
            created_at DateTime
        )
    Engine=MergeTree()
    ORDER BY (user_id, film_id, film_frame)
"""

CREATE_DATABASE = 'CREATE DATABASE IF NOT EXISTS ugc ON CLUSTER company_cluster'

INSERT_DATAS = 'INSERT INTO {database} VALUES'