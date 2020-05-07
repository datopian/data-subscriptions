from flask_restful import Resource, request
from flask import Response

from data_subscriptions.models import Subscription as Model
from data_subscriptions.notifications.ckan_metadata import CKANMetadata


def create_csv(dataset, columns):
    header = ",".join(columns)
    content = header + "\n"

    for data in dataset:
        row = ",".join(data.values())
        content += row + "\n"
    return content


def get_user(data_id, action):
    result = CKANMetadata(action, [data_id])()
    if data_id in result:
        return result[data_id]
    return {}


def prepare_stat(data):
    dataset_name = ""
    user_name = ""
    dataset = get_user(data.dataset_id, "package_show")
    user = get_user(data.user_id, "user_show")
    if "name" in dataset:
        dataset_name = dataset["name"]
    if "display_name" in user:
        user_name = user["display_name"]

    return {
        "subscribed_at": str(data.created_at),
        "user_id": data.user_id,
        "user_name": user_name,
        "dataset_id": data.dataset_id,
        "dataset_name": dataset_name,
    }


class Stat(Resource):
    def get(self):
        dataset = Model.query.all()
        result = map(prepare_stat, dataset)
        download = request.args.get("download")
        if download == "yes":
            columns = [
                "Subscribed At",
                "User ID",
                "Username",
                "Dataset ID",
                "Dataset Name",
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
