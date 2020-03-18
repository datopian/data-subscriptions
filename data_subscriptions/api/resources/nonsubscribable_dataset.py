from flask_restful import Resource

from data_subscriptions.models import NonsubscribableDataset
from data_subscriptions.extensions import db


class NonsubscribableDatasetResource(Resource):
    def get(self, dataset_id):
        dataset = NonsubscribableDataset.query.filter_by(
            dataset_id=dataset_id
        ).first_or_404()
        return {"dataset_id": dataset.dataset_id, "subscribable": False}

    def post(self, dataset_id):
        status = 200
        is_not_in_db = not db.session.query(
            NonsubscribableDataset.query.filter_by(dataset_id=dataset_id).exists()
        ).scalar()
        if is_not_in_db:
            db.session.add(NonsubscribableDataset(dataset_id=dataset_id))
            db.session.commit()
            status = 201
        return {"dataset_id": dataset_id, "subscribable": False}, status

    def delete(self, dataset_id):
        dataset = NonsubscribableDataset.query.filter_by(dataset_id=dataset_id).delete()
        return None, 204
