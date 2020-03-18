setup:
	cp .env.example .env
	docker-compose build
	docker-compose up -d
	docker-compose run --rm web data_subscriptions db upgrade

test:
	docker-compose run --rm web pytest -s

lint:
	docker-compose run --rm web black --check .
