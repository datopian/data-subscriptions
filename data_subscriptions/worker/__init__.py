import os

from celery import Celery
from celery.schedules import crontab

from data_subscriptions.worker.dataset_activity_list import DatasetActivityList

PULL_FREQUENCY = int(os.getenv("TIME_IN_SECONDS_BETWEEN_ACTIVITY_PULLS"))
BACKEND_URL = os.getenv("REDIS_URL")
BROKER_URL = os.getenv("RABBITMQ_URL")

app = Celery("tasks", backend=BACKEND_URL, broker=BROKER_URL)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(PULL_FREQUENCY, pull_latest_activities.s())


@app.task
def pull_latest_activities():
    DatasetActivityList().run()
