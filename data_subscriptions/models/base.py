from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import functions as func

from data_subscriptions.extensions import db


class Base:
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=func.now())
    updated_at = db.Column(
        db.DateTime(), nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<{type(self).__name__} id={self.id}>"


BaseModel = declarative_base(cls=Base)
