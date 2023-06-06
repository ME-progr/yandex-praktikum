# Укажите необходимую версию python
FROM python:3.11-slim

ENV APP_DIR /opt/app

# Выберите папку, в которой будут размещаться файлы проекта внутри контейнера
WORKDIR $APP_DIR

# Заведите необходимые переменные окружения
ENV DJANGO_SETTINGS_MODULE 'config.settings'
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Скопируйте в контейнер файлы, которые редко меняются
COPY requirements.txt requirements.txt

# Установите зависимости
RUN  apt-get update \
     && apt-get -y install libpq-dev gcc \
     && apt install -y netcat \
     && groupadd -r web \
     && useradd -d $APP_DIR -r -g web web \
     && chown web:web -R $APP_DIR \
     && mkdir $APP_DIR/static \
     && mkdir $APP_DIR/media \
     && pip install --upgrade pip \
     && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# Скопируйте всё оставшееся. Для ускорения сборки образа эту команду стоит разместить ближе к концу файла.
COPY . $APP_DIR

RUN chmod u+x $APP_DIR/start-billing.sh \
    && python manage.py collectstatic --noinput

USER web

ENTRYPOINT ["/opt/app/start-billing.sh"]