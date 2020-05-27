from data_subscriptions.models import Subscription, NonsubscribableDataset
import json


def test_get_dataset_subscription_200_subscription_exists(client, db, subscription):
    # Return 200 OK when subscription does exit
    db.session.add(subscription)
    db.session.commit()
    dataset_id = subscription.dataset_id
    user_id = subscription.user_id
    data = json.dumps(
        {
            "user_id": user_id,
            "dataset_id": dataset_id,
            "kind": "DATASET",
            "user_name": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.post(f"/api/v1/subscription_status", data=data)
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"dataset_id": dataset_id, "user_id": user_id, "kind": "DATASET"}


def test_get_new_datasets_subscription_200_subscription_exists(
    client, db, new_dataset_subscription
):
    # Return 200 OK when subscription to new dataset does exit
    db.session.add(new_dataset_subscription)
    db.session.commit()
    user_id = new_dataset_subscription.user_id
    data = json.dumps(
        {
            "user_id": user_id,
            "kind": "NEW_DATASETS",
            "user_name": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.post(f"/api/v1/subscription_status", data=data)
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"user_id": user_id, "kind": "NEW_DATASETS"}


def test_get_dataset_subscription_404_subscription_doesnt_exist(
    client, db, subscription
):
    # Return 404 NOT FOUND when subscription does not exist
    dataset_id = subscription.dataset_id
    user_id = subscription.user_id
    data = json.dumps(
        {
            "user_id": user_id,
            "dataset_id": dataset_id,
            "kind": "DATASET",
            "user_name": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.post(f"/api/v1/subscription_status", data=data)
    assert response.status_code == 404


def test_get_new_dataset_subscription_404_subscription_doesnt_exist(
    client, db, new_dataset_subscription
):
    # Return 404 NOT FOUND when subscription does not exist
    user_id = new_dataset_subscription.user_id
    data = json.dumps(
        {
            "user_id": user_id,
            "kind": "NEW_DATASETS",
            "user_name": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.post(f"/api/v1/subscription_status", data=data)
    assert response.status_code == 404


def test_post_subscription_201_new(client, db, subscription):
    # Return 201 CREATED when subscription is made.
    dataset_id = subscription.dataset_id
    user_id = subscription.user_id
    data = json.dumps(
        {
            "user_id": subscription.user_id,
            "dataset_id": dataset_id,
            "kind": "DATASET",
            "username": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.post(f"/api/v1/subscription", data=data)
    assert response.status_code == 201
    data = response.get_json()
    assert data["dataset_id"] == dataset_id
    assert data["user_id"] == user_id

    is_in_db = db.session.query(
        Subscription.query.filter_by(dataset_id=dataset_id, user_id=user_id).exists()
    ).scalar()
    assert is_in_db


def test_post_subscription_422_dataset_is_nonsubscribable(client, db, subscription):
    # Return 422 UNPROCESSABLE ENTITY when subscription made to nonsubscribable datsets.
    dataset_id = subscription.dataset_id
    user_id = subscription.user_id
    db.session.add(NonsubscribableDataset(dataset_id=dataset_id))
    db.session.commit()
    data = json.dumps(
        {
            "user_id": subscription.user_id,
            "dataset_id": dataset_id,
            "kind": "DATASET",
            "username": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.post(f"/api/v1/subscription", data=data)
    data = response.get_json()
    assert response.status_code == 422
    assert data["subscribed"] == False


def test_post_subscription_already_subscribed(client, db, subscription):
    # Return 422 UNPROCESSABLE ENTITY when already subscribed to the dataset.
    db.session.add(subscription)
    db.session.commit()
    user_id = subscription.user_id
    dataset_id = subscription.dataset_id
    data = json.dumps(
        {
            "user_id": subscription.user_id,
            "dataset_id": dataset_id,
            "kind": "DATASET",
            "username": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.post(f"/api/v1/subscription", data=data)
    data = response.get_json()
    assert response.status_code == 422
    assert data["subscribed"] == False


def test_post_new_dataset_subscription_already_subscribed(
    client, db, new_dataset_subscription
):
    # Return 422 UNPROCESSABLE ENTITY when already subscribed to the dataset.
    db.session.add(new_dataset_subscription)
    db.session.commit()
    user_id = new_dataset_subscription.user_id
    data = json.dumps(
        {
            "user_id": new_dataset_subscription.user_id,
            "kind": "NEW_DATASETS",
            "username": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.post(f"/api/v1/subscription", data=data)
    data = response.get_json()
    assert response.status_code == 422
    assert data["subscribed"] == False


def test_delete_unsubscribe(client, db, subscription):
    # Return 204 NO CONTENT when subscription deleted.
    db.session.add(subscription)
    db.session.commit()
    user_id = subscription.user_id
    dataset_id = subscription.dataset_id
    data = json.dumps(
        {
            "user_id": subscription.user_id,
            "dataset_id": dataset_id,
            "kind": "DATASET",
            "user_name": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.delete(f"/api/v1/subscription", data=data)
    assert response.status_code == 204


def test_delete_subscription_by_dataset(
    mocker, ckan_meta_fixture, client, db, all_subscription, all_subscription_list
):
    # Return 204 NO CONTENT when subscription deleted by dataset id.
    dispatcher = mocker.patch(
        "data_subscriptions.api.resources.subscribed_dataset.NotSubscribableNotifiationDispatcher"
    )

    dataset_id = all_subscription[0]["dataset_id"]
    response = client.delete(f"/api/v1/dataset/{dataset_id}")
    assert response.status_code == 204


def test_delete_subscription_by_non_exist_dataset(
    mocker, ckan_meta_fixture, client, db, all_subscription, all_subscription_list
):
    # Return 422 UNPROCESSABLE ENTITY when subscription delete by non exist dataset id.
    dataset_id = "nonexist-dataset-id"
    response = client.delete(f"/api/v1/dataset/{dataset_id}")
    assert response.status_code == 422


def test_delete_new_dataset_unsubscribe(client, db, new_dataset_subscription):
    # Return 204 NO CONTENT when subscription deleted.
    db.session.add(new_dataset_subscription)
    db.session.commit()
    user_id = new_dataset_subscription.user_id
    data = json.dumps(
        {
            "user_id": user_id,
            "kind": "NEW_DATASETS",
            "user_name": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.delete(f"/api/v1/subscription", data=data)
    assert response.status_code == 204


def test_delete_unsubscribe_doesnt_exist(client, db, subscription):
    # Return 422 UNPROCESSABLE ENTITY when delete subscription that doesn't exist.
    user_id = subscription.user_id
    dataset_id = subscription.dataset_id
    data = json.dumps(
        {
            "user_id": subscription.user_id,
            "dataset_id": dataset_id,
            "kind": "DATASET",
            "user_name": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.delete(f"/api/v1/subscription", data=data)
    assert response.status_code == 422


def test_delete_unsubscribe_new_dataset_doesnt_exist(
    client, db, new_dataset_subscription
):
    # Return 422 UNPROCESSABLE ENTITY when delete subscription that doesn't exist.
    user_id = new_dataset_subscription.user_id
    data = json.dumps(
        {
            "user_id": user_id,
            "kind": "NEW_DATASETS",
            "user_name": "julietezekwe",
            "email": "alice@example.com",
        }
    )
    response = client.delete(f"/api/v1/subscription", data=data)
    assert response.status_code == 422


def test_subsfription_without_email_or_username(client, db, new_dataset_subscription):
    # Return 422 UNPROCESSABLE ENTITY when delete subscription that doesn't exist.
    user_id = new_dataset_subscription.user_id
    data = json.dumps(
        {"user_id": user_id, "kind": "NEW_DATASETS", "user_name": "julietezekwe",}
    )
    response = client.delete(f"/api/v1/subscription", data=data)
    assert response.status_code == 422
