#!/bin/sh

python -u utils/wait_for_redis.py
python -u utils/wait_for_mongodb.py
pytest ./src/

exec "$@"