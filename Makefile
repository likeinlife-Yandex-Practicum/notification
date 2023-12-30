SOURCE_QUEUE := dead_letter
DEST_QUEUE := notify_task

up:
	docker compose up -d --build
	docker compose up -d --build

downv:
	docker compose down -v
	docker compose down -v

down:
	docker compose down
	docker compose down
	
dead-letter-setup:
	docker compose exec -it rabbit rabbitmqctl set_parameter shovel my-shovel \
	'{"src-protocol": "amqp091", "src-uri": "amqp://guest:guest@127.0.0.1:5672",  "src-queue": "$(SOURCE_QUEUE)",  "dest-protocol": "amqp091",  "dest-uri": "amqp://guest:guest@127.0.0.1:5672",  "dest-queue": "$(DEST_QUEUE)",  "dest-queue-args": {"x-queue-type": "quorum"}}'

up-notify:
	docker compose up -d rabbit postgres notification-user notification-notify --build

env:
	./env-setup.sh