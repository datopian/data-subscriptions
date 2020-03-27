setup:
	cp .env.example .env
	docker-compose build
	docker-compose up -d
	docker-compose run --rm web data_subscriptions db upgrade

test:
	docker-compose run --rm web pytest -vv --cov=data_subscriptions

lint:
	docker-compose run --rm web black --check .
