from flask_restful import Resource, request

from data_subscriptions.extensions import db

from data_subscriptions.models import Subscription as Model


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
        data = request.get_json( force = True )
        
        return {
            "dataset_id": dataset_id,
            "user_id": data["user_id"],
        }
