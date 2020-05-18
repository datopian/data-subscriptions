from itertools import groupby
from operator import itemgetter

from data_subscriptions.extensions import db

QUERY = """
-- Activity - New packages
SELECT
  kind,
  user_id,
  activity->>'object_id' AS dataset_id,
  dataset_name,
  user_name,
  activity->>'activity_type' AS activity_type,
  activity
FROM
  dataset_activity_list,
  json_array_elements(dataset_activity_list.blob) AS activity
  JOIN subscription ON (
    activity->>'activity_type' = 'new package'
  )
WHERE
  subscription.kind = 'NEW_DATASETS' AND
  (activity->>'timestamp')::timestamptz > :start_time

UNION ALL

-- Activity - Dataset updates
SELECT
  kind,
  user_id,
  activity->>'object_id' AS dataset_id,
  dataset_name,
  user_name,
  activity->>'activity_type' AS activity_type,
  activity
FROM
  dataset_activity_list,
  json_array_elements(dataset_activity_list.blob) AS activity
  JOIN subscription ON (
    activity->>'object_id' = subscription.dataset_id
  )
WHERE
  (subscription.kind = 'DATASET') OR (subscription.kind IS NULL) AND
  activity->>'activity_type' != 'new package' AND
  (activity->>'timestamp')::timestamptz > :start_time

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
