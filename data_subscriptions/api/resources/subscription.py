from flask_restful import Resource, request
from http import HTTPStatus

from data_subscriptions.extensions import db

from data_subscriptions.models import Subscription as Model, NonsubscribableDataset
from data_subscriptions.notifications.ckan_metadata import CKANMetadata


def can_subscribe(user_id, dataset_id=False):
    if dataset_id:
        is_not_in_db = not db.session.query(
            Model.query.filter_by(dataset_id=dataset_id,
                                  user_id=user_id).exists()
        ).scalar()
        if is_not_in_db:
            is_subscribable = not db.session.query(
                NonsubscribableDataset.query.filter_by(
                    dataset_id=dataset_id).exists()
            ).scalar()
            return is_subscribable
        return is_not_in_db
    else:
        return not db.session.query(
            Model.query.filter_by(kind="NEW_DATASETS",
                                  user_id=user_id).exists()
        ).scalar()


def get_subscription_by_dataset_id(dataset_id, user_id):
    return Model.query.filter_by(dataset_id=dataset_id, user_id=user_id).first()


def get_ckan_metadata(data_id, action, attr):
    result = CKANMetadata(action, [data_id])()
    if data_id in result and attr in result[data_id]:
        return result[data_id][attr]
    return ""


def remove_sub(is_subscribed):
    db.session.delete(is_subscribed)
    db.session.commit()
    return None, 204


def remove_dataset_subscription(dataset_id, user_id):
    is_subscribed = Model.query.filter_by(
        dataset_id=dataset_id, user_id=user_id, kind="DATASET",
    ).one_or_none()
    if is_subscribed:
        return remove_sub(is_subscribed)
    else:
        return None, 422


def remove_new_dataset_subscription(user_id):
    is_subscribed = Model.query.filter_by(
        user_id=user_id, kind="NEW_DATASETS"
    ).one_or_none()
    if is_subscribed:
        return remove_sub(is_subscribed)
    else:
        return None, 422


def is_missing_post_params(data, keys):

    return not all(k in data for k in keys)


class SubscriptionStatus(Resource):
    def __init__(self):
        self.DATASET = "DATASET"
        self.NEW_DATASETS = "NEW_DATASETS"

    def post(self):
        data = request.get_json(force=True)
        keys = ["user_id", "kind"]
        if is_missing_post_params(data, keys):
            return {"error": "invalid parameters"}, HTTPStatus.UNPROCESSABLE_ENTITY
        user_id = data["user_id"]
        kind = data["kind"]
        response = {}
        if kind == self.DATASET:
            dataset_id = data["dataset_id"]
            subscription = Model.query.filter_by(
                dataset_id=dataset_id, user_id=user_id, kind=kind,
            ).first_or_404()
            response = {
                "dataset_id": subscription.dataset_id,
                "phone_number": subscription.phone_number,
                "user_id": subscription.user_id,
                "kind": self.DATASET,
            }
        else:
            subscription = Model.query.filter_by(
                kind=self.NEW_DATASETS, user_id=user_id,
            ).first_or_404()
            response = {
                "user_id": subscription.user_id,
                "kind": self.NEW_DATASETS,
            }
        return response


class Subscription(Resource):
    def __init__(self):
        self.DATASET = "DATASET"
        self.NEW_DATASETS = "NEW_DATASETS"
        self.DELETE = "DELETE"
        self.POST = "POST"
        self.PUT = "PUT"

    def put(self):
        response = {}
        data = request.get_json(force=True)
        keys = ["email", "user_id", "username", "kind"]
        if is_missing_post_params(data, keys):
            return {"error": "invalid parameters"}, HTTPStatus.UNPROCESSABLE_ENTITY
        dataset_id = data["dataset_id"]
        user_id = data["user_id"]
        subscription = get_subscription_by_dataset_id(dataset_id, user_id)
        if subscription is None:
            return {"error": "could not find subscription"}, HTTPStatus.NOT_FOUND
        phone_number = data["phone_number"] if "phone_number" in data else None
        if phone_number:
            setattr(subscription, "phone_number", phone_number)
        else:
            setattr(subscription, "phone_number", None)
        db.session.add(subscription)
        db.session.commit()
        db.session.refresh(subscription)

    def post(self):
        response = {}
        data = request.get_json(force=True)
        status = 422
        keys = ["email", "user_id", "username", "kind"]
        if is_missing_post_params(data, keys):
            return {"error": "invalid parameters"}, HTTPStatus.UNPROCESSABLE_ENTITY
        email = data["email"]
        user_id = data["user_id"]
        user_name = data["username"]
        phone_number = data["phone_number"] if "phone_number" in data else None
        kind = data["kind"]

        if kind == self.DATASET and can_subscribe(user_id, data["dataset_id"]):
            dataset_id = data["dataset_id"]
            dataset_name = get_ckan_metadata(
                dataset_id, "package_show", "name")
            db.session.add(
                Model(
                    user_id=user_id,
                    email=email,
                    kind=self.DATASET,
                    dataset_id=dataset_id,
                    dataset_name=dataset_name,
                    user_name=user_name,
                    phone_number=phone_number,
                )
            )
            db.session.commit()
            status = 201
            response = (
                {
                    "dataset_id": dataset_id,
                    "user_id": user_id,
                    "kind": self.DATASET,
                    "user_name": user_name,
                    "subscribed": True,
                },
                status,
            )
        elif kind == self.NEW_DATASETS and can_subscribe(user_id):
            db.session.add(
                Model(
                    user_id=user_id,
                    user_name=user_name,
                    email=email,
                    kind=self.NEW_DATASETS,
                )
            )
            db.session.commit()
            status = 201
            response = (
                {"subscribed": True, "user_id": user_id,
                    "kind": self.NEW_DATASETS, },
                status,
            )
        else:
            response = (
                {"subscribed": False},
                status,
            )
        return response

    def delete(self):
        data = request.get_json(force=True)
        keys = ["user_id", "kind"]
        if is_missing_post_params(data, keys):
            return {"error": "invalid parameters"}, HTTPStatus.UNPROCESSABLE_ENTITY
        user_id = data["user_id"]
        kind = data["kind"]
        response = {}
        status = 204
        if kind == self.DATASET:
            dataset_id = data["dataset_id"]
            response = remove_dataset_subscription(dataset_id, user_id)
        else:
            response = remove_new_dataset_subscription(user_id)
        return response
