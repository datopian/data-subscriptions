import datetime as dt
import itertools

import pytest

from data_subscriptions.notifications.activity_groups.dataset_updates import (
    QUERY as DATASET_UPDATES_QUERY,
)
from data_subscriptions.notifications.activity_groups.new_packages import (
    QUERY as NEW_PACKAGES_QUERY,
)
from data_subscriptions.models import *

TIMESTAMP_BEFORE = "2020-01-31T23:59:59.999999"
TIMESTAMP = "2020-02-01T00:00:00.000000"
TIMESTAMP_AFTER = "2020-02-01T00:00:00.000001"


def seed_db_with_fixtures(db):
    db.session.add(
        DatasetActivityList(blob=activity_list_blob(), collected_at=dt.datetime.now())
    )
    for record in subscriptions():
        db.session.add(record)
        db.session.commit()


def activity_list_blob():
    blob = record_list_for_combinations(
        {
            "activity_type": ["new package", "changed package"],
            "timestamp": [TIMESTAMP_BEFORE, TIMESTAMP_AFTER],
            "object_id": ["a", "b"],
        }
    )
    return blob


def subscriptions():
    xs = []
    for kind in ["DATASET", "NEW_DATASETS"]:
        dataset_ids = ["a"] if kind == "DATASET" else [None]
        for user_id in ["1", "2"]:
            for dataset_id in dataset_ids:
                xs.append(
                    Subscription(
                        dataset_id=dataset_id,
                        user_id=user_id,
                        user_name=f"User {user_id}",
                        dataset_name=dataset_id,
                        kind=kind,
                    )
                )
    xs.append(
        Subscription(
            dataset_id="b",
            user_id="3",
            user_name=f"User 3",
            dataset_name="b",
            kind="DATASET",
        )
    )
    return xs


def record_list_for_combinations(options):
    keys = options.keys()
    values = (options[key] for key in keys)
    blob = []
    for combination in itertools.product(*values):
        blob.append(dict(zip(keys, combination)))
    return blob


def test_filter_new_packages(db):
    seed_db_with_fixtures(db)

    records = db.session.execute(NEW_PACKAGES_QUERY, {"start_time": TIMESTAMP})
    records = [dict(zip(records.keys(), x)) for x in records]
    expected = [
        {
            "kind": "NEW_DATASETS",
            "user_id": "1",
            "dataset_id": "a",
            "dataset_name": None,
            "user_name": "User 1",
            "activity_type": "new package",
            "activity": {
                "activity_type": "new package",
                "timestamp": "2020-02-01T00:00:00.000001",
                "object_id": "a",
            },
        },
        {
            "kind": "NEW_DATASETS",
            "user_id": "2",
            "dataset_id": "a",
            "dataset_name": None,
            "user_name": "User 2",
            "activity_type": "new package",
            "activity": {
                "activity_type": "new package",
                "timestamp": "2020-02-01T00:00:00.000001",
                "object_id": "a",
            },
        },
        {
            "kind": "NEW_DATASETS",
            "user_id": "1",
            "dataset_id": "b",
            "dataset_name": None,
            "user_name": "User 1",
            "activity_type": "new package",
            "activity": {
                "activity_type": "new package",
                "timestamp": "2020-02-01T00:00:00.000001",
                "object_id": "b",
            },
        },
        {
            "kind": "NEW_DATASETS",
            "user_id": "2",
            "dataset_id": "b",
            "dataset_name": None,
            "user_name": "User 2",
            "activity_type": "new package",
            "activity": {
                "activity_type": "new package",
                "timestamp": "2020-02-01T00:00:00.000001",
                "object_id": "b",
            },
        },
    ]
    assert records == expected


def test_filter_dataset_updates(db):
    seed_db_with_fixtures(db)

    records = db.session.execute(DATASET_UPDATES_QUERY, {"start_time": TIMESTAMP})
    records = [dict(zip(records.keys(), x)) for x in records]
    expected = [
        {
            "kind": "DATASET",
            "user_id": "2",
            "dataset_id": "a",
            "dataset_name": "a",
            "user_name": "User 2",
            "activity_type": "changed package",
            "activity": {
                "activity_type": "changed package",
                "timestamp": "2020-02-01T00:00:00.000001",
                "object_id": "a",
            },
        },
        {
            "kind": "DATASET",
            "user_id": "1",
            "dataset_id": "a",
            "dataset_name": "a",
            "user_name": "User 1",
            "activity_type": "changed package",
            "activity": {
                "activity_type": "changed package",
                "timestamp": "2020-02-01T00:00:00.000001",
                "object_id": "a",
            },
        },
        {
            "kind": "DATASET",
            "user_id": "3",
            "dataset_id": "b",
            "dataset_name": "b",
            "user_name": "User 3",
            "activity_type": "changed package",
            "activity": {
                "activity_type": "changed package",
                "timestamp": "2020-02-01T00:00:00.000001",
                "object_id": "b",
            },
        },
    ]
    assert records == expected
