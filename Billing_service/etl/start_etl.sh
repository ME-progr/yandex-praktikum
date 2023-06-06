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

wait_pg_table()
{
  HOST=$1
  PORT=$2
  DB_NAME=$3
  USER_NAME=$4
  PASSWORD=$5
  SCHEMA_NAME=$6
  TABLE_NAME=$7

while ! PGPASSWORD=$PASSWORD psql -h $HOST -p $PORT -U $USER_NAME -d $DB_NAME -c "\dt $SCHEMA_NAME.$TABLE_NAME" | grep $TABLE_NAME; do
    echo 'Table not exists'
    sleep 0.1
done

  echo "$SCHEMA_NAME.$TABLE_NAME exists"
}


if [ ${MOVIES_DB_TYPE} = "postgres" ]
  then
    wait_database $MOVIES_DB_HOST $MOVIES_DB_PORT $MOVIES_DB_TYPE
fi

if [ ${BILLING_DB_TYPE} = "postgres" ]
  then
    wait_database $BILLING_DB_HOST $BILLING_DB_PORT $BILLING_DB_TYPE
fi

if [ ${STATE_STORAGE_TYPE} = "redis" ]
  then
    wait_database $REDIS_HOST $REDIS_PORT $STATE_STORAGE_TYPE
fi

wait_pg_table $MOVIES_DB_HOST $MOVIES_DB_PORT $MOVIES_DB_NAME $MOVIES_DB_USER $MOVIES_DB_PASSWORD $MOVIES_SCHEMA_NAME "film_work"

wait_pg_table $BILLING_DB_HOST $BILLING_DB_PORT $BILLING_DB_NAME $BILLING_DB_USER $BILLING_DB_PASSWORD $BILLING_SCHEMA_NAME "filmwork"


python ./start_etl.py

exec "$@"
