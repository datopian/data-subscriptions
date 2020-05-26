from flask_restful import Resource, request

from data_subscriptions.extensions import db
from data_subscriptions.models import Subscription as Model
from data_subscriptions.schemas import SubscriptionSchema as Schema
from data_subscriptions.notifications.not_subscribable_notification_dispatcher import (
    NotSubscribableNotifiationDispatcher,
)


class User(Resource):
    def get(self, user_id):
        datasets = (
            db.session.query(Model).filter_by(user_id=user_id, kind="DATASET").all()
        )
        datasetsSchema = Schema(many=True)
        if datasets:
            subscribed_datasets = {"subscriptions": datasetsSchema.dump(datasets)}
            return subscribed_datasets, 200
        return None, 404


class Dataset(Resource):
    def delete(self, dataset_id):
        datasets = Model.query.filter_by(dataset_id=dataset_id, kind="DATASET").all()
        if len(datasets) > 0:
            Model.query.filter_by(dataset_id=dataset_id, kind="DATASET").delete()
            for item in datasets:
                NotSubscribableNotifiationDispatcher(dataset_id, item.user_id)()
            db.session.commit()
        else:
            return None, 422
        return None, 204
