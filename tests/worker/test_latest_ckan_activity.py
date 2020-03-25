import datetime as dt
import pytest

from data_subscriptions.worker.latest_ckan_activity import LatestCKANActivity


@pytest.fixture
def activity_list():
    xs = []
    for day in range(31, 0, -1):
        xs.append({"timestamp": f"2020-01-{str(day).zfill(2)}T00:00:00.000000"})
    return xs


@pytest.fixture
def mock_api_1(mocker, activity_list):
    api = mocker.MagicMock(name="ckan_api")
    api.return_value.action.recently_changed_packages_activity_list.side_effect = [
        activity_list,
        [],
    ]
    return api


@pytest.fixture
def mock_api_2(mocker, activity_list):
    api = mocker.MagicMock(name="ckan_api")
    api.return_value.action.recently_changed_packages_activity_list.side_effect = [
        activity_list[:10],
        activity_list[10:20],
        activity_list[20:30],
        activity_list[30:],
        [],
    ]
    return api


@pytest.fixture
def mock_api_3(mocker, activity_list):
    api = mocker.MagicMock(name="ckan_api")
    api.return_value.action.recently_changed_packages_activity_list.return_value = []
    return api


def test_fetch_when_api_returns_all_the_data_in_a_single_request(
    mocker, mock_api_1, activity_list
):
    api = mocker.patch(
        "data_subscriptions.worker.latest_ckan_activity.RemoteCKAN", new=mock_api_1
    )
    subject = LatestCKANActivity(proposed_limit=100)
    response = subject.fetch()

    call_args_list = (
        api.return_value.action.recently_changed_packages_activity_list.call_args_list
    )
    assert call_args_list == [
        mocker.call(limit=100, offset=0),
        mocker.call(limit=31, offset=31),
    ]
    assert response == activity_list


def test_fetch_when_api_has_smaller_limit_than_proposed_limit(
    mocker, mock_api_2, activity_list
):
    api = mocker.patch(
        "data_subscriptions.worker.latest_ckan_activity.RemoteCKAN", new=mock_api_2
    )
    subject = LatestCKANActivity(proposed_limit=100)
    response = subject.fetch()

    call_args_list = (
        api.return_value.action.recently_changed_packages_activity_list.call_args_list
    )
    assert call_args_list == [
        mocker.call(limit=100, offset=0),
        mocker.call(limit=10, offset=10),
        mocker.call(limit=10, offset=20),
        mocker.call(limit=10, offset=30),
    ]
    assert response == activity_list


def test_fetch_when_api_has_no_data(mocker, mock_api_3, activity_list):
    api = mocker.patch(
        "data_subscriptions.worker.latest_ckan_activity.RemoteCKAN", new=mock_api_3
    )
    subject = LatestCKANActivity(proposed_limit=100)
    response = subject.fetch()

    call_args_list = (
        api.return_value.action.recently_changed_packages_activity_list.call_args_list
    )
    assert call_args_list == [
        mocker.call(limit=100, offset=0),
    ]
    assert response == []


def test_fetch_when_api_has_data_in_expected_time_range(
    mocker, mock_api_1, activity_list
):
    api = mocker.patch(
        "data_subscriptions.worker.latest_ckan_activity.RemoteCKAN", new=mock_api_1
    )
    subject = LatestCKANActivity(start_time=dt.datetime(2020, 1, 1))
    response = subject.fetch()

    call_args_list = (
        api.return_value.action.recently_changed_packages_activity_list.call_args_list
    )
    assert call_args_list == [
        mocker.call(limit=1000, offset=0),
        mocker.call(limit=31, offset=31),
    ]
    assert response == activity_list


def test_fetch_when_api_has_part_of_its_data_in_expected_time_range(
    mocker, mock_api_1, activity_list
):
    api = mocker.patch(
        "data_subscriptions.worker.latest_ckan_activity.RemoteCKAN", new=mock_api_1
    )
    subject = LatestCKANActivity(start_time=dt.datetime(2020, 1, 10))
    response = subject.fetch()

    call_args_list = (
        api.return_value.action.recently_changed_packages_activity_list.call_args_list
    )
    assert call_args_list == [
        mocker.call(limit=1000, offset=0),
        mocker.call(limit=31, offset=31),
    ]
    assert response == activity_list[:22]


def test_fetch_when_api_has_no_data_in_expected_time_range(
    mocker, mock_api_2, activity_list
):
    api = mocker.patch(
        "data_subscriptions.worker.latest_ckan_activity.RemoteCKAN", new=mock_api_2
    )
    subject = LatestCKANActivity(start_time=dt.datetime(2021, 1, 1))
    response = subject.fetch()

    call_args_list = (
        api.return_value.action.recently_changed_packages_activity_list.call_args_list
    )
    assert call_args_list == [
        mocker.call(limit=1000, offset=0),
    ]
    assert response == []
