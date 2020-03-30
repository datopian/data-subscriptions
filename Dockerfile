FROM python:3.8.2

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y \
	python3-psycopg2

COPY requirements.txt requirements-dev.txt setup.py ./
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
RUN pip install -e .

RUN useradd -ms /bin/bash app
RUN chown -R app .
USER app

COPY data_subscriptions data_subscriptions/
COPY migrations migrations/

EXPOSE 5500

CMD ["gunicorn", "-b", "0.0.0.0:5500", "data_subscriptions.wsgi:app"]
