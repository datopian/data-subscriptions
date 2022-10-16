from enum import Enum

from data_subscriptions.extensions import db
from data_subscriptions.models.base import BaseModel


class Kind(Enum):
    DATASET = "dataset"
    NEW_DATASETS = "new_datasets"


class Subscription(db.Model, BaseModel):
    dataset_id = db.Column(db.Text(), nullable=True)
    user_id = db.Column(db.Text(), nullable=False)
    kind = db.Column(db.Enum(Kind), nullable=True)
    user_name = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(), nullable=False)
    dataset_name = db.Column(db.Text(), nullable=True)
    phone_number = db.Column(db.Text(), nullable=True)
    __table_args__ = (db.UniqueConstraint("dataset_id", "user_id"),)

    def __repr__(self):
        return (
            "<Subscription dataset_id=%s user_id=%s kind=%s user_name=%s email=%s dataset_name=%s phone_number=%s>"
            % (
                self.dataset_id,
                self.user_id,
                self.kind,
                self.user_name,
                self.email,
                self.dataset_name,
                self.phone_number,
            )
        )
