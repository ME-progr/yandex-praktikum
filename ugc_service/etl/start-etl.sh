#!/bin/sh

wait_database()
{
  HOST=$1
  PORT=$2
  TYPE=$3

  echo "Waiting for $TYPE..."

  while ! nc -z $HOST $PORT; do
    sleep 0.1
  done

  echo "$TYPE started"
}

if [ ${EVENT_DB_TYPE} = "kafka" ]
  then
    wait_database $KAFKA_HOST $KAFKA_PORT $EVENT_DB_TYPE
fi

if [ ${CLICKHOUSE_DB_TYPE} = "clickhouse" ]
  then
    wait_database $CLICKHOUSE_HOST $CLICKHOUSE_PORT $CLICKHOUSE_DB_TYPE
fi

if [ ${CACHE_DB_TYPE} = "redis-kafka" ]
  then
    wait_database $REDIS_KAFKA_HOST $REDIS_KAFKA_PORT $CACHE_DB_TYPE
fi

python ./main.py

exec "$@"
