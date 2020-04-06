from data_subscriptions.extensions import db


QUERY = """
SELECT
    details
FROM
    dataset_activity_list,
    json_array_elements(dataset_activity_list.blob) AS details
WHERE
    last_activity_created_at > :start_time AND
    details->>'object_id' in (
        SELECT dataset_id
        FROM subscription
        WHERE user_id = :user_id
    );
"""


class ActivityForUser:
    def __init__(self, user_id, start_time):
        self.user_id = user_id
        self.start_time = start_time

    def __call__(self):
        result = db.session.execute(
            QUERY, {"start_time": self.start_time, "user_id": self.user_id}
        )
        activity_list = []
        for row in result:
            activity_list.append(row[0])
        return activity_list
