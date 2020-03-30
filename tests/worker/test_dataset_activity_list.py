import datetime as dt

import pytest
from freezegun import freeze_time


from data_subscriptions.models.dataset_activity_list import DatasetActivityList as Model
from data_subscriptions.worker.dataset_activity_list import DatasetActivityList


@pytest.fixture(scope="module")
def subject():
    return DatasetActivityList()


def test_run(mocker, subject):
    mocker.patch.object(subject, "extract")
    mocker.patch.object(subject, "load")
    subject.run()
    subject.extract.assert_called_once()
    subject.load.assert_called_once()


@freeze_time("2020-03-01")
def test_extract(mocker, subject, db):
    ckan_activity = mocker.patch(
        "data_subscriptions.worker.dataset_activity_list.LatestCKANActivity"
    )
    ckan_blob = [{"timestamp": "2020-01-01T00:00:00.000000"}]
    ckan_activity.return_value.fetch.return_value = ckan_blob
    subject.extract()

    ckan_activity.return_value.fetch.assert_called_once()
    assert subject.blob == ckan_blob
    assert subject.collected_at == dt.datetime(2020, 3, 1)


@freeze_time("2020-03-01")
def test_extract_without_previous_activity_in_local_db(mocker, subject, db):
    ckan_activity = mocker.patch(
        "data_subscriptions.worker.dataset_activity_list.LatestCKANActivity"
    )
    ckan_blob = [{"timestamp": "2020-01-01T00:00:00.000000"}]
    ckan_activity.return_value.fetch.return_value = ckan_blob
    subject.extract()

    one_day_ago = dt.datetime(2020, 2, 29)
    ckan_activity.assert_called_once_with(start_time=one_day_ago)


def test_extract_with_previous_activity_in_local_db(
    mocker, subject, db, dataset_activity_list
):
    ckan_activity = mocker.patch(
        "data_subscriptions.worker.dataset_activity_list.LatestCKANActivity"
    )
    ckan_activity.return_value.fetch.return_value = []

    db.session.add(dataset_activity_list)
    db.session.commit()

    subject.extract()

    last_activity_created_at = dt.datetime(2020, 2, 1)
    ckan_activity.assert_called_once_with(start_time=last_activity_created_at)


def test_load_empty_blob_from_latest_ckan_activity(mocker, subject):
    ckan_activity = mocker.patch(
        "data_subscriptions.worker.dataset_activity_list.LatestCKANActivity"
    )
    ckan_activity.return_value.fetch.return_value = []
    db = mocker.patch("data_subscriptions.worker.dataset_activity_list.db")

    subject.load()
    db.session.add.assert_called_once()

    new_row = db.session.add.call_args_list[0][0][0].__dict__
    assert new_row["last_activity_created_at"] is None


def test_load_nonempty_blob_from_latest_ckan_activity(mocker, subject):
    ckan_blob = [{"timestamp": "2020-01-01T00:00:00.000000"}]
    subject.blob = ckan_blob
    db = mocker.patch("data_subscriptions.worker.dataset_activity_list.db")

    subject.load()
    db.session.add.assert_called_once()

    new_row = db.session.add.call_args_list[0][0][0].__dict__
    assert new_row["last_activity_created_at"] == dt.datetime(2020, 1, 1)
