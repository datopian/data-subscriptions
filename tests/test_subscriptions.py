from data_subscriptions.models import Subscription
import json

def test_get_subscription_200_subscription_exists(client, db, subscription):
    # Return 200 OK when subscription does exit
    db.session.add(subscription)
    db.session.commit()
    dataset_id = subscription.dataset_id
    user_id = subscription.user_id
    response = client.get(f"/api/v1/subscription/{dataset_id}?user_id={user_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"dataset_id": dataset_id, "user_id": user_id}


def test_get_subscription_404_subscription_doesnt_exist(client, db, subscription):
    # Return 404 NOT FOUND when subscription does not exist
    dataset_id = subscription.dataset_id
    user_id = subscription.user_id
    response = client.get(f"/api/v1/subscription/{dataset_id}?user_id={user_id}")
    assert response.status_code == 404

def test_post_subscription_200_new(client, db, subscription):
    # Return 200 OK when subscription is made.
    dataset_id = subscription.dataset_id
    user_id = subscription.user_id
    data = json.dumps({"user_id": subscription.user_id})
    response = client.post(f"/api/v1/subscription/{dataset_id}", data = data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["dataset_id"] == dataset_id
    assert data["user_id"] == user_id

    is_in_db = db.session.query(
		Subscription.query.filter_by(dataset_id=dataset_id, user_id=user_id).exists()
    ).scalar()
    assert is_in_db

