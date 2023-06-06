FROM python:3.11

ENV APP_DIR /etl

WORKDIR $APP_DIR

COPY requirements.txt $APP_DIR

RUN  apt-get update \
     && apt-get -y install libpq-dev gcc \
     && apt-get install acl \
     && apt install -y netcat \
     && groupadd -r web \
     && useradd -d $APP_DIR -r -g web web \
     && chown web:web -R $APP_DIR

RUN pip install -r $APP_DIR/requirements.txt

COPY . $APP_DIR

RUN chmod u+x $APP_DIR/start-etl.sh

ENTRYPOINT ["/etl/start-etl.sh"]