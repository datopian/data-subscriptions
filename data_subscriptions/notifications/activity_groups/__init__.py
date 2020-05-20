from itertools import groupby
from operator import itemgetter

from data_subscriptions.extensions import db
from data_subscriptions.notifications.activity_groups.dataset_updates import (
    QUERY as DATASET_UPDATES_QUERY,
)
from data_subscriptions.notifications.activity_groups.new_packages import (
    QUERY as NEW_PACKAGES_QUERY,
)

QUERY = f"""
{NEW_PACKAGES_QUERY}

UNION ALL

{DATASET_UPDATES_QUERY}

ORDER BY
  user_id,
  dataset_id;
"""


class ActivityList:
    """
    Collect a list of users to be notified, and relevant dataset activity.
    """

    def __init__(self, start_time):
        self.start_time = start_time
        self._all = None

    def by_user(self):
        keys = self.all.keys()
        all_with_keys = map(lambda row: dict(zip(keys, row)), self.all)
        return groupby(all_with_keys, itemgetter("user_id"))

    @property
    def all(self):
        if not self._all:
            self._all = db.session.execute(QUERY, {"start_time": self.start_time})
        return self._all
