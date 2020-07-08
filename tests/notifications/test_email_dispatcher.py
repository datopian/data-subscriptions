import datetime as dt

import pytest

from data_subscriptions.notifications import email_dispatcher


@pytest.fixture
def api_response(mocker):
    return mocker.MagicMock(name="Response", status_code=202)


def test_call(mocker, api_response):
    APIClient = mocker.patch.object(email_dispatcher, "SendGridAPIClient")
    APIClient.return_value.send.return_value = api_response
    subject = email_dispatcher.EmailDispatcher("alice@example.com")

    subject({"message": "it works!"})
    APIClient.return_value.send.assert_called_once()
