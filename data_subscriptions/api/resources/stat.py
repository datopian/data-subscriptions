from flask_restful import Resource, request
from flask import Response

from data_subscriptions.models import Subscription as Model


def create_csv(subscription, columns):
    header = ",".join(columns)
    content = header + "\n"

    for data in subscription:
        row = ",".join(data.values())
        content += row + "\n"
    return content


def prepare_stat(subscription):
    return {
        "subscribed_at": str(subscription.created_at),
        "user_id": subscription.user_id,
        "user_name": subscription.user_name,
        "dataset_id": subscription.dataset_id,
        "dataset_name": subscription.dataset_name,
        "kind": str(subscription.kind)[5:],
    }


class Stat(Resource):
    def get(self):
        subscriptions = Model.query.all()
        result = map(prepare_stat, subscriptions)
        download = request.args.get("download")
        if download == "yes":
            columns = [
                "Subscribed At",
                "User ID",
                "Username",
                "Dataset ID",
                "Dataset Name",
                "Kind",
            ]
            csv = create_csv(result, columns)
            return Response(
                csv,
                mimetype="text/csv",
                headers={
                    "Content-disposition": "attachment; filename=data_subscribers.csv"
                },
            )
        return {"result": list(result)}
