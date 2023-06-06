FROM python:3.11-slim

ENV APP_DIR /opt/etl
ENV PYTHONPATH "${PYTHONPATH}:/opt"

WORKDIR $APP_DIR

ENV ETL_SETTINGS_MODULE 'config.settings'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  apt-get update \
     && apt-get -y install libpq-dev gcc \
     && apt-get install acl \
     && apt install -y netcat \
     && apt -y install postgresql \
     && groupadd -r web \
     && useradd -d $APP_DIR -r -g web web \
     && chown web:web -R $APP_DIR \
     && pip install --upgrade pip \
     && rm -rf /var/lib/apt/lists/*

RUN pip install -r $APP_DIR/requirements.txt

COPY . $APP_DIR

RUN chmod u+x $APP_DIR/start_etl.sh

ENTRYPOINT ["/opt/etl/start_etl.sh"]