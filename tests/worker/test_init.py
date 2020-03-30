from data_subscriptions import worker as subject


def test_pull_latest_activities(mocker):
    DatasetActivityList = mocker.patch.object(subject, "DatasetActivityList")
    subject.pull_latest_activities()
    DatasetActivityList.return_value.run.assert_called_once()
