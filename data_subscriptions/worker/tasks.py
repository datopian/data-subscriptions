import os
from contextlib import contextmanager

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_subscriptions.app import create_app
from data_subscriptions.extensions import db
from data_subscriptions.notifications.batch_dispatcher import BatchDispatcher
from data_subscriptions.worker.dataset_activity_list import DatasetActivityList


BROKER_URL = os.getenv("REDIS_URL", default=os.getenv("REDISTOGO_URL"))
if not BROKER_URL:
    password = os.getenv("redis-password")
    host = os.getenv("REDIS_HOST")
    BROKER_URL = f"redis://default:{password}@{host}:6379/0"

PULL_FREQUENCY = int(os.getenv("TIME_IN_SECONDS_BETWEEN_ACTIVITY_PULLS"))
NOTIFICATION_FREQUENCY = int(
    os.getenv("TIME_IN_SECONDS_BETWEEN_NOTIFICATION_DELIVERIES")
)

app = Celery("tasks", broker=BROKER_URL)


class Database:
    def __init__(self):
        self.app = create_app()

    @contextmanager
    def session(self):
        with self.app.app_context():
            yield

            db.session.commit()
            db.session.close()
            db.get_engine().dispose()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(PULL_FREQUENCY, pull_latest_activities.s())
    sender.add_periodic_task(NOTIFICATION_FREQUENCY, dispatch_notifications.s())


@app.task
def pull_latest_activities():
    with Database().session():
        DatasetActivityList()()


@app.task
def dispatch_notifications():
    with Database().session():
        BatchDispatcher()()
