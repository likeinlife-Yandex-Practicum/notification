SOURCE_QUEUE := dead_letter
DEST_QUEUE := user_provided

up:
	docker compose up -d --build

downv:
	docker compose down -v

down:
	docker compose down

test:
	docker compose -f ./tests/docker-compose.yaml up --abort-on-container-exit --exit-code-from tests --attach tests --build
	
dead-letter-setup:
	docker compose exec -it rabbit rabbitmqctl set_parameter shovel my-shovel \
	'{"src-protocol": "amqp091", "src-uri": "amqp://guest:guest@127.0.0.1:5672",  "src-queue": "$(SOURCE_QUEUE)",  "dest-protocol": "amqp091",  "dest-uri": "amqp://guest:guest@127.0.0.1:5672",  "dest-queue": "$(DEST_QUEUE)",  "dest-queue-args": {"x-queue-type": "quorum"}}'

up-notify:
	docker compose up -d rabbit postgres notification-user notification-notify notification-rabbit mailpit --build

env:
	./env-setup.sh