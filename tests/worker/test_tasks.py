from data_subscriptions.worker import tasks as subject


def test_pull_latest_activities(mocker):
    DatasetActivityList = mocker.patch.object(subject, "DatasetActivityList")
    subject.pull_latest_activities()
    DatasetActivityList.return_value.assert_called_once()


def test_dispatch_notifications(mocker):
    BatchDispatcher = mocker.patch.object(subject, "BatchDispatcher")
    subject.dispatch_notifications()
    BatchDispatcher.return_value.assert_called_once()
