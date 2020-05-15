from flask_restful import Resource, request
from flask import Response

from data_subscriptions.models import Subscription as Model


def create_csv(dataset, columns):
    header = ",".join(columns)
    content = header + "\n"

    for data in dataset:
        row = ",".join(data.values())
        content += row + "\n"
    return content


def prepare_stat(data):
    return {
        "subscribed_at": str(data.created_at),
        "user_id": data.user_id,
        "user_name": data.user_name,
        "dataset_id": "N/A" if data.dataset_id is None else data.dataset_id,
        "dataset_name": "N/A" if data.dataset_name is None else data.dataset_name,
        "kind": str(data.kind)[5:],
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
