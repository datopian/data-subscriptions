import os

from celery import Celery
from celery.schedules import crontab

from data_subscriptions.notifications.batch_dispatcher import BatchDispatcher
from data_subscriptions.worker.dataset_activity_list import DatasetActivityList

BACKEND_URL = os.getenv("REDIS_URL", default=os.getenv("REDISTOGO_URL"))
BROKER_URL = os.getenv("RABBITMQ_URL", default=os.getenv("CLOUDAMQP_URL"))

PULL_FREQUENCY = int(os.getenv("TIME_IN_SECONDS_BETWEEN_ACTIVITY_PULLS"))
NOTIFICATION_FREQUENCY = int(
    os.getenv("TIME_IN_SECONDS_BETWEEN_NOTIFICATION_DELIVERIES")
)

app = Celery("tasks", backend=BACKEND_URL, broker=BROKER_URL)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(PULL_FREQUENCY, pull_latest_activities.s())
    sender.add_periodic_task(NOTIFICATION_FREQUENCY, dispatch_notifications.s())


@app.task
def pull_latest_activities():
    DatasetActivityList()()


@app.task
def dispatch_notifications():
    BatchDispatcher()()
