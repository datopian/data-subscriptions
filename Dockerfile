FROM python:3.8

RUN mkdir /code
WORKDIR /code

COPY requirements.txt requirements-dev.txt setup.py ./
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
RUN pip install -e .

COPY data_subscriptions data_subscriptions/
COPY migrations migrations/

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "data_subscriptions.wsgi:app"]
