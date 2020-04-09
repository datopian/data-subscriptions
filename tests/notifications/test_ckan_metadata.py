import ckanapi.errors

from data_subscriptions.notifications.ckan_metadata import CKANMetadata


def test_call_returns_empty_hash_for_empty_ids():
    subject = CKANMetadata("package_show", [])
    assert subject() == {}


def test_call_returns_metadata_for_entities_of_the_same_type(mocker):
    api = mocker.patch("data_subscriptions.notifications.ckan_metadata.RemoteCKAN")

    subject = CKANMetadata("package_show", ["x", "y", "z"])
    assert subject() == {
        "x": api().action.package_show(id="x"),
        "y": api().action.package_show(id="y"),
        "z": api().action.package_show(id="z"),
    }


def test_call_removes_duplicates_from_ids(mocker):
    api = mocker.patch("data_subscriptions.notifications.ckan_metadata.RemoteCKAN")

    subject = CKANMetadata("package_show", ["x", "y", "x"])
    response = subject()
    assert api().action.package_show.call_count == 2
    assert response == {
        "x": api().action.package_show(id="x"),
        "y": api().action.package_show(id="y"),
    }


def test_call_doesnt_include_key_for_failed_requests(mocker):
    api = mocker.patch("data_subscriptions.notifications.ckan_metadata.RemoteCKAN")
    api.return_value.action.package_show.side_effect = [
        {"name": "A Dataset"},
        ckanapi.errors.NotFound,
        {"name": "Another Dataset"},
    ]

    subject = CKANMetadata("package_show", {"x", "y", "z"})
    response = subject()
    assert len(response) == 2
    assert {"name": "A Dataset"} in response.values()
    assert {"name": "Another Dataset"} in response.values()


def test_call_logs_failed_requests(mocker, caplog):
    api = mocker.patch("data_subscriptions.notifications.ckan_metadata.RemoteCKAN")
    api.return_value.action.package_show.side_effect = [
        {"name": "A Dataset"},
        ckanapi.errors.NotFound,
    ]

    subject = CKANMetadata("package_show", {"x", "y"})
    subject()
    assert len(caplog.records) == 1
