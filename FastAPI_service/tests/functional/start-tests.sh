#!/bin/sh

python -u utils/wait_for_es.py
python -u utils/wait_for_redis.py
pytest ./src/

exec "$@"
