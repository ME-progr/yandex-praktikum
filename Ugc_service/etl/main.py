"""Модуль запуска ETL процесса Kafka -> Clickhouse"""

import os

from etl_manager import ETL
from services.adapter import AdapterKafkaToClickhouse
from services.extractor import KafkaExtractor
from services.loader import ClickhouseLoader
from utils import logs
from utils.connection import Clients

from sentry_sdk import init


if __name__ == '__main__':

    init(
        os.getenv('SENTRY_DSN'),
        traces_sample_rate=1.0
    )

    logger = logs.get_stream_logger()

    extractor = KafkaExtractor(Clients.kafka_consumer)
    adapter = AdapterKafkaToClickhouse()
    loader = ClickhouseLoader(Clients.clickhouse)

    with ETL(extractor=extractor, loader=loader, adapter=adapter) as process:
        process.start(logger)
