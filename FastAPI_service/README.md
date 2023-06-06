Авторы:
 - [Антон](https://github.com/mistandok)
 - [Михаил](https://github.com/Mikhail-Kushnerev)
 - [Евгений](https://github.com/ME-progr)

## Общие действия
Необходимо создать конфигурационные файлы с актуальными значениями паролей, пользователей и т.п.. 
Для вашего удобства в вышеописанных директориях уже лежат файлы с актуальными параметрами для запуска приложения, на реальном проекте в репозитории бы были размещены только файлы-примеры:
 - `./docker_app/config/etl_process/.env.prod` (пример `./docker_app/config/etl_process/.env.prod.example`)
 - `./docker_app/config/admin_panel/.env.prod.db` (пример `./docker_app/config/admin_panel/.env.prod.db.example`)
 - `./docker_app/config/admin_panel/.env.prod` (пример `./docker_app/config/admin_panel/.env.prod.example`)
 - `./docker_app/config/fastapi_project/.env.prod` (пример `./docker_app/config/fastapi_project/.env.prod.example`)
 - `./docker_app/config/functional_tests/.env.prod` (пример `./docker_app/config/functional_tests/.env.prod.example`)

## Для запуска тестов в контейнере необходимо проделать действия, описанные ниже.

Файл настройки `docker-compose.tests.yml` располагается по пути `./docker_app/docker-compose.tests.yml`.  Через него необходимо запускать тестирование приложения в контейнере.

1) Перейти в папку `./docker_app`, из нее в консоли последовательно выполнить указанные команды.
2) Удаление контейнеров и томов (если уже устанавливали их ранее) - `docker-compose -f docker-compose.tests.yml down -v`
3) Запуск контейнеров с перестройкой image - `docker-compose -f docker-compose.tests.yml up --exit-code-from tests` (Нужно учитывать тот факт, что Elasticsearch стартует не так быстро, как хотелось бы. Поэтому отследить состояние etl контейнера можно через его логи: `docker logs *container-id*`, как только там появятся сообщения, что все базы данных стартанули, то etl-процесс и fast-api сервис стартанут.)
4) После того как тесты пройдут и контейнеры завершат свою работу, можно зайти в логи контейнера с тестами и убедиться, что все они пройдены.


## Для запуска приложения в контейнере необходимо проделать действия, описанные ниже.

Файл настройки `docker-compose.prod.yml` располагается по пути `./docker_app/docker-compose.prod.yml`.  Через него необходимо запускать приложение.
Файл настройки `docker-compose.yml` необходим нам для локального тестирования приложения, его запускать не нужно.


1) Перейти в папку `./docker_app`, из нее в консоли последовательно выполнить указанные команды.
2) Удаление контейнеров и томов (если уже устанавливали их ранее) - `docker-compose -f docker-compose.prod.yml down -v`
3) Запуск контейнеров с перестройкой image - `docker-compose -f docker-compose.prod.yml up -d --build` (Нужно учитывать тот факт, что Elasticsearch стартует не так быстро, как хотелось бы. Поэтому отследить состояние etl контейнера можно через его логи: `docker logs *container-id*`, как только там появятся сообщения, что все базы данных стартанули, то etl-процесс и fast-api сервис стартанут.)
4) Загрузка тестовых данных в БД (в базе появятся данные. После этого нужно немного подождать, чтобы ETL-процессы перегнали данные в Elasticsearch) - `docker-compose -f docker-compose.prod.yml exec service python manage.py loaddata dumpdata.json`
5) Для проверкир работы API можно перейти по ссылке [localhost/api/openapi/](http://127.0.0.1:80/api/openapi/), там же можно увидеть описание API
6) Для входа в админку можно перейти по ссылке [localhost/admin](http://127.0.0.1:80/admin/) и воспользоваться парой `логин/пароль: admin/admin`.