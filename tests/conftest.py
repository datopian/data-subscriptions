import json

import pytest

from data_subscriptions.models import NonsubscribableDataset, Subscription
from data_subscriptions.app import create_app
from data_subscriptions.extensions import db as _db


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def nonsubscribable_dataset():
    return NonsubscribableDataset(dataset_id="b72159fe-67d8-4ea7-8313-af2bf9210799")


@pytest.fixture
def subscription():
    return Subscription(
        dataset_id="b72159fe-67d8-4ea7-8313-af2bf9210799", user_id="123"
    )


@pytest.fixture
def subscription_list():
    return [
        {"dataset_id": "b72159fe-67d8-4ea7-8313-af2bf9210799", "user_id": "user1"},
        {"dataset_id": "b72159fe-67d8-4ea7-8313-af2bf92107100", "user_id": "user1"},
        {"dataset_id": "b72159fe-67d8-4ea7-8313-af2bf92107101", "user_id": "user2"},
        {"dataset_id": "b72159fe-67d8-4ea7-8313-af2bf92107102", "user_id": "user2"},
    ]
