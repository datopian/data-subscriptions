from flask_restful import Resource, request

from data_subscriptions.extensions import db

from data_subscriptions.models import Subscription as Model, NonsubscribableDataset


def can_subscribe(user_id, dataset_id):
    is_not_in_db = not db.session.query(
        Model.query.filter_by(dataset_id=dataset_id, user_id=user_id).exists()
    ).scalar()
    if is_not_in_db:
        is_subscribable = not db.session.query(
            NonsubscribableDataset.query.filter_by(dataset_id=dataset_id).exists()
        ).scalar()
        return is_subscribable
    return is_not_in_db


class Subscription(Resource):
    def get(self, dataset_id):
        user_id = request.args.get("user_id")
        subscription = Model.query.filter_by(
            dataset_id=dataset_id, user_id=user_id
        ).first_or_404()
        return {
            "dataset_id": subscription.dataset_id,
            "user_id": subscription.user_id,
        }

    def post(self, dataset_id):
        data = request.get_json(force=True)
        user_id = data["user_id"]
        status = 422
        if can_subscribe(user_id, dataset_id):
            db.session.add(Model(dataset_id=dataset_id, user_id=user_id))
            db.session.commit()
            status = 201
        return {"dataset_id": dataset_id, "user_id": user_id}, status

    def delete(self, dataset_id):
        data = request.get_json(force=True)
        user_id = data["user_id"]
        status = 204
        is_subscribed = Model.query.filter_by(
            dataset_id=dataset_id, user_id=user_id
        ).one_or_none()
        if is_subscribed:
            db.session.delete(is_subscribed)
            db.session.commit()
        else:
            return None, 422
        return None, status