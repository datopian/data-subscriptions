from data_subscriptions.extensions import db


class NonsubscribableDataset(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    dataset_id = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<NonsubscribableDataset dataset_id=%s>" % self.dataset_id
