from flask_restful import Resource, request

from data_subscriptions.extensions import db

from data_subscriptions.models import Subscription as Model
from data_subscriptions.schemas import SubscriptionSchema as Schema
import json


class SubscribedDataset(Resource):
    def get(self, user_id):
        datasets = db.session.query(Model).filter_by(user_id=user_id).all()
        datasetsSchema = Schema(many=True)
        if datasets:
            subscribed_datasets = {
                "user": {"subscriptions": datasetsSchema.dump(datasets)}
            }
            return subscribed_datasets, 200
        return None, 404
