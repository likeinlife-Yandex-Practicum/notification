SOURCE_QUEUE := dead_letter
DEST_QUEUE := user_provided

up:
	docker compose up -d --build

downv:
	docker compose down -v

down:
	docker compose down

prod:
	docker compose -f docker-compose-prod.yaml up -d --build

test:
	docker compose -f ./tests/docker-compose.yaml up --abort-on-container-exit --exit-code-from tests --attach tests --build

up-notify:
	docker compose up -d rabbit postgres notification-user notification-notify notification-rabbit mailpit --build

env:
	./env-setup.sh

migrate:
	docker compose exec auth-api alembic -c /opt/app/alembic.ini upgrade head

create-admin:
	docker compose exec auth-api python -m cli admin create $(email) $(password)

init-service-accounts:
	docker compose exec auth-api python -m cli service init-service-accounts

create-user:
	docker compose exec auth-api python -m cli user create $(n)