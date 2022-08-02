![1](https://github.com/alklim912/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# foodgram
# Продуктовый помощник
доступен по адресу http://51.250.20.183/recipes

## Описание:
Простая регистрация, удобный интерфейс, умная и удобная логика работы.

## Функционал:
- регистрация пользователя
- смена пароля
- создание рецепта
- теги
- поиск ингредиентов
- подписки на авторов
- избранное
- виртуальная корзина
- список ингредиентов к покупке

## Процесс установки:

 * Для запуска на чистой машине на Ubuntu:
 * Установите docker:

 ```sudo apt install docker.io```

 * Загрузите и установите плагин Compose CLI, запустите:

 ```DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}```
 ```mkdir -p $DOCKER_CONFIG/cli-plugins```
 ```curl -SL https://github.com/docker/compose/releases/download/v2.7.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose```
 Эта команда загружает последний выпуск Docker Compose (из репозитория выпусков Compose) и устанавливает Compose для активного пользователя в $HOMEкаталоге.

 * Примените исполняемые разрешения к двоичному файлу:

 ```chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose```


 * Перенесите конфигурационные файлы nginx и docker compose:

 ```scp docker-compose.yml <username>@<host>:/~/docker-compose.yml```
 ```scp nginx.conf <username>@<host>:/~/nginx.conf```

 * Пропишите внешний IP вашего сервера в конфиге nginx в блоке "server_name"

### Шаблон наполнения env-файла:

 DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
 
 DB_NAME=<имя базы данных>
 
 POSTGRES_USER=<логин для подключения к базе данных>
 
 POSTGRES_PASSWORD=<пароль для подключения к БД>
 
 DB_HOST=<название сервиса (контейнера)>
 
 DB_PORT=<порт для подключения к БД>
 
 SECRET_KEY=<значение ключа из файла settings.py>


 Сборка образов, пуш в докерхаб и деплой на боевой сервер осуществляется автоматизировано с использованием workflow github.

 После первого деплоя на прод среде необходимо выполнить следующие команды:

 ```$ docker compose exec backend python manage.py makemigrations```
 
 ```docker compose exec backend python manage.py migrate```
 
 ```$ docker compose exec backend python manage.py createsuperuser```
 
 ```$ docker compose exec backend python manage.py collectstatic --no-input```
 
 ```$ docker compose exec backend python jsoninbd.py```



 ### Разработчик: [Александр Климентьев](https://github.com/alklim912)
