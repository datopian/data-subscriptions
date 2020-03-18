from data_subscriptions.models import NonsubscribableDataset


def test_get_nonsubscribable_datasets_404(client, db, nonsubscribable_dataset):
    # Return 404 NOT FOUND (subscribable status) for datasets not in database
    dataset_id = nonsubscribable_dataset.dataset_id
    response = client.get(f"/api/v1/nonsubscribable_datasets/{dataset_id}")
    assert response.status_code == 404


def test_get_nonsubscribable_datasets_200(client, db, nonsubscribable_dataset):
    # Return 200 OK and nonsubscribable status for datasets in database
    db.session.add(nonsubscribable_dataset)
    db.session.commit()

    dataset_id = nonsubscribable_dataset.dataset_id
    response = client.get(f"/api/v1/nonsubscribable_datasets/{dataset_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["dataset_id"] == dataset_id
    assert not data["subscribable"]


def test_post_nonsubscribable_datasets_new(client, db, nonsubscribable_dataset):
    # Return 201 CREATED for datasets not present in database yet
    dataset_id = nonsubscribable_dataset.dataset_id
    response = client.post(f"/api/v1/nonsubscribable_datasets/{dataset_id}")
    assert response.status_code == 201

    data = response.get_json()
    assert data["dataset_id"] == dataset_id
    assert not data["subscribable"]


def test_post_nonsubscribable_datasets_existing(client, db, nonsubscribable_dataset):
    # Return 200 OK for datasets already present in database
    db.session.add(nonsubscribable_dataset)
    db.session.commit()

    dataset_id = nonsubscribable_dataset.dataset_id
    response = client.post(f"/api/v1/nonsubscribable_datasets/{dataset_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["dataset_id"] == dataset_id
    assert not data["subscribable"]


def test_delete_nonsubscribable_datasets_existing(client, db, nonsubscribable_dataset):
    # Return 204 NO CONTENT for datasets present in database
    db.session.add(nonsubscribable_dataset)
    db.session.commit()

    dataset_id = nonsubscribable_dataset.dataset_id
    response = client.delete(f"/api/v1/nonsubscribable_datasets/{dataset_id}")
    assert response.status_code == 204

    is_not_in_db = not db.session.query(
        NonsubscribableDataset.query.filter_by(dataset_id=dataset_id).exists()
    ).scalar()
    assert is_not_in_db
