# UGS service

Авторы:
 - [Антон](https://github.com/mistandok)
 - [Михаил](https://github.com/Mikhail-Kushnerev)
 - [Евгений](https://github.com/ME-progr)
 - [Илья](https://github.com/Bexram)

В рамках текущего спринта было реализовано несколько задач:
1) Был произведен сравнительный анализ двух колоночных баз данных: Vertica и Clickhouse. Произведен анализ докумнетоориентированной базы MongoDB. Результаты исследования можно посмотреть, если перейти из корня проекта в папку: /storages_research/research_results. В файле [tests.logs](https://github.com/ME-progr/yandex-praktikum/blob/main/Ugc_service/storages_research/research_results/tests.logs) можно увидеть результаты выполнения нескольких тестов. Также в этой папке можно посмотреть графическую интерпритацию результатов. Сам анализ произведен в [README](https://github.com/ME-progr/yandex-praktikum/blob/main/Ugc_service/storages_research/README.md) файле. 
2) Реализован сервис UGC для работы с клиентскими событиями и контентом. Схему можно посмотреть на [diagrams.net](https://app.diagrams.net/#G1p3ByXTYNoDsIPpHmOoWbEr1nSTl_YSkd). Реализован ETL процесс, который перегоняет события из Kafka в Clickhouse

Реализованы следующий ручки:
 - ручка для записи события в кафку (Сейчас есть только одно событие: фрейм фильма, на котором отсановился пользователь при просмотре).
 - ручки для работы с рейтингом фильма: выставление оценок фильму, обновление оценки, удаление оценки, получение оценки, получение среднепользовательской оценки для заданного фильма.
 - ручки для работы с отзывами фильма: добавление отзыва, обновление отзыва, удаление отзыва, получение отзыва, список отзывов к фильму с постраничной навигацией.
 - ручки для работы с закладками пользователя: добавление фильма в закладки, удаление фильма из закладок, получение списка закладок с постраничной навигацией.

Длё работы с большинством ручек необходима авторизация. Токены 4 пользователей для проверки доступны ниже.   

Также для проекта был настроен **CI/CD**, в рамках которого:
- осуществляется автоматическая проверка линтерами (**flake8**, **mypy**);
- результат проверка сохраняется в **html**-файлы;
- телеграмм-бот присылает пуш-уведомление о новом **pull-request**.


## Содержание

- [технологии](#технологии)
- [запуск](#запуск)
- [авторы](#авторы)

## Технологии

- Python
- FastAPI
- ClickHouse
- Kafka
- Redis
- MongoDB
- Docker
- Nginx

## Запуск

Запуск сервиса осуществляется из директории `/docker_app`

- тесты:

    ```docker
    docker-compose -f docker-compose.tests.yml down -v
    docker-compose -f docker-compose.tests.yml up --exit-code-from tests
    ```

- проект:

    ```docker
    docker-compose -f docker-compose.prod.yml down -v
    docker-compose -f docker-compose.prod.yml up -d --build
    ```
    Настройка кластера для mongodb
   - ```docker exec -it mongocfg1 bash -c 'mongosh < /scripts/init-configserver.js'```
   - ```docker exec -it mongors1n1 bash -c 'mongosh < /scripts/init-shard01.js'```
   - ```docker exec -it mongors2n1 bash -c 'mongosh < /scripts/init-shard02.js'```
   - ```docker exec -it mongos1 bash -c 'mongosh < /scripts/init-router.js'```

    Сервис и список доступных урлов: [http://127.0.0.1/api/openapi](http://127.0.0.1/api/openapi)

    <details>
      <summary>
        <h3>Токены разных пользователей для работы с сервисом:</h3>
      </summary>
      1) eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1ODI5LCJqdGkiOiJiODRkZDA2Zi03MDMxLTRmZTQtOTA4OC1lZDIxMzcwYjkyNjgiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiJkZmM3Y2I3YS0yNTlhLTQ2MDktYmU0NS0wODdkMzA5ZDU0NWMiLCJ1c2VyX3JvbGVzIjpbImFkbWluIl0sInVzZXJfYWdlbnQiOiJtb2JpbGUiLCJyZWZyZXNoX2p0aSI6IjljZDdhZWVlLWMzOTMtNGQ3NC1iMGU2LWUyZTZiMDg0ZWE1MCJ9LCJuYmYiOjE2Nzk3MzU4MjksImV4cCI6MTY3OTc0MzAyOX0.EmLwK_Riuhf03iOkeDhpXWk8CFcZtfZ_tCnRRjsd9Nw </br>
      2) eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1ODY4LCJqdGkiOiIwMmJkNDdmMy1iY2NmLTRkY2ItYWY1OS1jODhmYTI3M2JjYTMiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiIwNmY1YmRkZS00ZjUwLTQ5NTYtYTQ5ZC1hZTA3Mzc5ODA5YjYiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwidXNlcl9hZ2VudCI6Im1vYmlsZSIsInJlZnJlc2hfanRpIjoiMWNlZWYwZmMtYjBmZi00MGUyLTg1N2QtOTk1OWRlNjA0ZDFlIn0sIm5iZiI6MTY3OTczNTg2OCwiZXhwIjoxNjc5NzQzMDY4fQ.y8u7zzHHNl-jxkFkhObe63Lqe9Hv0Hn2WR15Q-fX6t4 </br>
      3) eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1OTE2LCJqdGkiOiIwZTRjNTdmMC00NmNjLTQxYjktOTBiZS01M2Y5ODk5YjQ1ZjQiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiI5ODY1Nzg1ZS05MDQzLTQwMmEtOGU0YS01ODM3OGY5ZDQ0MjgiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwidXNlcl9hZ2VudCI6Im1vYmlsZSIsInJlZnJlc2hfanRpIjoiMzlmZDc3YTAtOTdjMC00OTk1LWIzNDUtZDkzODA2MTA2MzJhIn0sIm5iZiI6MTY3OTczNTkxNiwiZXhwIjoxNjc5NzQzMTE2fQ.SWq1TTRZisARXM3NlCocsUCDh8FAU1_0vsPCHBvm4w0 </br>
      4) eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc5NzM1OTQ4LCJqdGkiOiJhNWY5MDA3ZS1lOWI5LTRhM2ItODk4OC03ZWQ3ODhjOTg4ZjciLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjp7InVzZXJfaWQiOiIzM2NiZjRhNy02ZGFlLTQ4NmItYjk2My0xNjcyYTU4MTg5NGQiLCJ1c2VyX3JvbGVzIjpbInVzZXIiXSwidXNlcl9hZ2VudCI6Im1vYmlsZSIsInJlZnJlc2hfanRpIjoiMzgxMWU5MGItNGEzZC00ZDFmLWE5ZDktMmY3NzUyMTM1YzI1In0sIm5iZiI6MTY3OTczNTk0OCwiZXhwIjoxNjc5NzQzMTQ4fQ.kPrHu2S1sQbwTeUFnur7mTPG4K7fRgKCDWkHhYbh7E4 </br>
    </details>

[в начало](#проектная-работа-8-спринта)
