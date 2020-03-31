import datetime as dt
from dateutil import tz

from data_subscriptions.app import create_app
from data_subscriptions.extensions import db
from data_subscriptions.models.dataset_activity_list import DatasetActivityList as Model
from data_subscriptions.worker.latest_ckan_activity import LatestCKANActivity


class DatasetActivityList:
    def __init__(self):
        self.app = create_app()

    def __call__(self):
        self.extract()
        self.load()

    def extract(self):
        self.collected_at = dt.datetime.now()
        self.blob = LatestCKANActivity(start_time=self.start_time())()

    def load(self):
        with self.app.app_context():
            db.session.add(self.build_data_activity_list())
            db.session.commit()

    def start_time(self):
        time_column = Model.last_activity_created_at
        with self.app.app_context():
            time = (
                db.session.query(time_column)
                .filter(time_column.isnot(None))
                .order_by(time_column.desc())
                .limit(1)
                .scalar()
            )
        return time or self.__time_range_for_initial_extraction()

    def build_data_activity_list(self):
        if len(self.blob) > 0:
            last_activity = self.blob[0]
            last_activity_created_at = dt.datetime.fromisoformat(
                last_activity["timestamp"]
            )
        else:
            last_activity_created_at = None
        return Model(
            blob=self.blob,
            collected_at=self.collected_at,
            last_activity_created_at=last_activity_created_at,
        )

    def __time_range_for_initial_extraction(self):
        return dt.datetime.now() - dt.timedelta(days=1)
