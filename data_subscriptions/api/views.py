from flask import Blueprint, current_app, jsonify
from flask_restful import Api

from data_subscriptions.api.resources import (
    NonsubscribableDataset,
    Subscription,
    User,
    Stat,
    SubscriptionStatus,
    Dataset,
)

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(
    NonsubscribableDataset, "/nonsubscribable_datasets/<string:dataset_id>",
)

api.add_resource(
    Subscription, "/subscription",
)

api.add_resource(
    SubscriptionStatus, "/subscription_status",
)

api.add_resource(
    User, "/user/<string:user_id>",
)

api.add_resource(
    Dataset, "/dataset",
)

api.add_resource(
    Stat, "/stat",
)
