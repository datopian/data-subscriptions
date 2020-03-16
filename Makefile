setup:
	cp -n .env.example .env
	docker-compose build
	docker-compose up -d
	docker-compose exec web data_subscriptions db upgrade
	docker-compose exec web data_subscriptions init
	docker-compose exec web data_subscriptions db migrate

test:
	docker-compose run --rm web pytest -s

lint:
	docker-compose run --rm web black --check .
