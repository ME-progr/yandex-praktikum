"""Модуль проверяет состояине Elasticsearch."""

from time import sleep
import sys

import backoff
import psycopg2
from psycopg2 import OperationalError

from settings import BILLING_PG_DSL, AUTH_PG_DSL, DB_SETTINGS


@backoff.on_exception(backoff.expo, OperationalError)
def wait_psql(dsl: dict, schema_name: str, table_name: str):
    conn = psycopg2.connect(**dsl)
    cursor = conn.cursor()

    while True:
        cursor.execute(f'''SELECT EXISTS (
                       SELECT FROM information_schema.tables 
                       WHERE  table_schema = '{schema_name}'
                       AND    table_name   = '{table_name}'
                       );''')
        is_table_exists = cursor.fetchone()[0]

        if is_table_exists:
            break
        else:
            sleep(1)

    conn.close()


if __name__ == '__main__':
    print('waiting for AUTH PostgreSQL...', file=sys.stdout)
    wait_psql(AUTH_PG_DSL, DB_SETTINGS.auth_schema, 'user')
    print('AUTH PostgreSQL was started', file=sys.stdout)

    print('waiting for BILLING PostgreSQL...', file=sys.stdout)
    wait_psql(BILLING_PG_DSL, DB_SETTINGS.billing_schema, 'filmwork')
    print('BILLING PostgreSQL was started', file=sys.stdout)
