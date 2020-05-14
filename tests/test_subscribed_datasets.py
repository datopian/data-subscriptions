from data_subscriptions.models import Subscription, NonsubscribableDataset
import json


def test_get_subscribed_datasets_200(client, db, subscription_list):
    # Return 200 OK for users with an existing subscription list.
    for sub in subscription_list:
        db.session.add(
            Subscription(
                dataset_id=sub["dataset_id"],
                user_id=sub["user_id"],
                user_name="julietezekwe1",
                kind="DATASET",
            )
        )
        db.session.commit()
    user_id = subscription_list[0]["user_id"]
    response = client.get(f"/api/v1/user/{user_id}")
    data = response.get_json()
    assert data == {"subscriptions": [subscription_list[0], subscription_list[1]]}
    assert response.status_code == 200


def test_get_subscribed_datasets_nonexits_user_404(client, db, subscription_list):
    # Return 404 NOT FOUND for users who are not subscribing to any dataset.
    for sub in subscription_list:
        db.session.add(
            Subscription(
                dataset_id=sub["dataset_id"],
                user_id=sub["user_id"],
                user_name="julietezekwe1",
                kind="DATASET",
            )
        )
        db.session.commit()
    user_id = "user4"  # non existing user
    response = client.get(f"/api/v1/user/{user_id}")
    assert response.status_code == 404
