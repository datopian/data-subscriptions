from data_subscriptions.extensions import db
from data_subscriptions.models.base import BaseModel


class NonsubscribableDataset(db.Model, BaseModel):
    dataset_id = db.Column(db.Text(), nullable=False, unique=True)

    def __repr__(self):
        return "<NonsubscribableDataset dataset_id=%s>" % self.dataset_id
