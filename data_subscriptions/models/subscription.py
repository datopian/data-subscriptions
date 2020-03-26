from data_subscriptions.extensions import db
from data_subscriptions.models.base import BaseModel


class Subscription(db.Model, BaseModel):
    dataset_id = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Text(), nullable=False)

    __table_args__ = (db.UniqueConstraint("dataset_id", "user_id"),)

    def __repr__(self):
        return "<Subscription dataset_id=%s user_id=%s>" % (
            self.dataset_id,
            self.user_id,
        )
