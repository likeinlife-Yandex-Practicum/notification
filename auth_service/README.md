# Описание

Auth service сделан для авторизации и работы с ролями пользователей

# Установка

- `git clone https://github.com/likeinlife/Auth_sprint_2/.git`
- Скопировать файл `./docker-composes/.env.example` в файл `./docker-composes/.env`
- через Makefile выполнить команды:
  - `make env` - подготовит .env фа
  - `make up`
  - `make migrate`
  - `make create-admin email=<email> password=<password>`

# Запуск/остановка

- `make up` - запуск
- `make down` - удалить созданные контейнеры
- `make downv` - удалить созданные контейнеры, включая volumes

# Тестирование

- `make test`
- `make down-test`

# URLs

- auth: http://localhost/auth/api/openapi
- jaeger: http://localhost:16686/
