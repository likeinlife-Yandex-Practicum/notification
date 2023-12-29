# Описание

Сервис отправки уведомлений для пользователя.
На данный момент реализовано уведомление по SMTP.
Сервис реализован по принципу pipeline, прослойками между микро-сервисами которого служат очереди RabbitMQ. 

# Авторы

* [@likeinlife](https://github.com/likeinlife)
* [@maxim-zaitsev](https://github.com/maxim-zaitsev)
* [@yandexwork](https://github.com/yandexwork)

## Вклад @likeinlife

- Оформление репозитория
- Создание диаграм
- Конфигурирование переменных окружения
- Пайплайн сервиса нотификации: получение юзеров, отправка уведомлений
- Настройка RabbitMQ: dead-letter-queue, exchanges, queues

## Вклад @maxim-zaitsev

- Создание админ-панели
- Создание сервиса регулярных уведомлений
- Конфигурирование nginx

## Вклад @yandexwork

- Написание АПИ
- Написание тестов АПИ

# Запуск

1. make env - скопировать sample.env в .env
2. В .env файле заменить переменные `SMTP_LOGIN`, `SMTP_PASSWORD` на свои (предполагается использование SMTP yandex, но можно заменить и `SMTP_HOST`, `SMTP_PORT`)
3. make up - запустить контейнеры
4. make dead-letter-setup - настроить Dead Letter Queue

# Тестирование

TODO

# URLs

1. admin panel: http://127.0.0.1/admin
2. api: http://127.0.0.1/api