setup:
	cp .env.example .env
	docker-compose build
	docker-compose up -d
	docker-compose run --rm web data_subscriptions db upgrade
	docker-compose run --rm web data_subscriptions init
	docker-compose run --rm web data_subscriptions db migrate

test:
	docker-compose run --rm web pytest -s

lint:
	docker-compose run --rm web black --check .
