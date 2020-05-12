from flask_restful import Resource, request

from data_subscriptions.extensions import db
from data_subscriptions.models import Subscription as Model
from data_subscriptions.schemas import SubscriptionSchema as Schema


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
