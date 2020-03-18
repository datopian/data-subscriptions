from flask_restful import Resource

from data_subscriptions.extensions import db
from data_subscriptions.models import NonsubscribableDataset as Model


class NonsubscribableDataset(Resource):
    def get(self, dataset_id):
        dataset = Model.query.filter_by(dataset_id=dataset_id).first_or_404()
        return {"dataset_id": dataset.dataset_id, "subscribable": False}

    def post(self, dataset_id):
        status = 200
        is_not_in_db = not db.session.query(
            Model.query.filter_by(dataset_id=dataset_id).exists()
        ).scalar()
        if is_not_in_db:
            db.session.add(Model(dataset_id=dataset_id))
            db.session.commit()
            status = 201
        return {"dataset_id": dataset_id, "subscribable": False}, status

    def delete(self, dataset_id):
        dataset = Model.query.filter_by(dataset_id=dataset_id).delete()
        db.session.commit()
        return None, 204
