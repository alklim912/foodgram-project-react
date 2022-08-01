# praktikum_new_diplom
Чтобы загрузить и установить плагин Compose CLI, запустите:

 DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
 mkdir -p $DOCKER_CONFIG/cli-plugins
 curl -SL https://github.com/docker/compose/releases/download/v2.7.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
Эта команда загружает последний выпуск Docker Compose (из репозитория выпусков Compose) и устанавливает Compose для активного пользователя в $HOMEкаталоге.

Установить:

Docker Compose для всех пользователей вашей системы, замените ~/.docker/cli-pluginsна /usr/local/lib/docker/cli-plugins.
Другая версия Compose, замените v2.7.0ее версией Compose, которую вы хотите использовать.
Примените исполняемые разрешения к двоичному файлу:

 chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

 