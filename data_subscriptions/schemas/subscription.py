from data_subscriptions.extensions import db, ma


class SubscriptionSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "dataset_id")
