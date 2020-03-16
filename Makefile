.PHONY: init init-migration build run db-migrate test

init:  build run
	docker-compose exec web data_subscriptions db upgrade
	docker-compose exec web data_subscriptions init
	@echo "Init done, containers running"

build:
	docker-compose build

run:
	docker-compose up -d

db-migrate:
	docker-compose exec web data_subscriptions db migrate

db-upgrade:
	docker-compose exec web data_subscriptions db upgrade

test:
	docker-compose run --rm web pytest

lint:
	docker-compose run --rm web black --check .
