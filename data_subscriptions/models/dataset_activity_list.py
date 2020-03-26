from sqlalchemy.sql import functions as func
from sqlalchemy.types import JSON

from data_subscriptions.extensions import db

from data_subscriptions.models.base import BaseModel


class DatasetActivityList(db.Model, BaseModel):
    blob = db.Column(JSON())
    last_activity_created_at = db.Column(db.DateTime())
    collected_at = db.Column(db.DateTime(), nullable=False)
