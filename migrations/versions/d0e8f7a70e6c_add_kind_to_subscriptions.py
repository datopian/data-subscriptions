"""add_kind_to_subscriptions

Revision ID: d0e8f7a70e6c
Revises: 89316d8bd746
Create Date: 2020-05-06 21:32:10.590634

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "d0e8f7a70e6c"
down_revision = "89316d8bd746"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    subscription_types = postgresql.ENUM("DATASET", "NEW_DATASETS", name="kind")
    subscription_types.create(op.get_bind())
    # ### end Alembic commands ###
    op.add_column(
        "subscription",
        sa.Column(
            "kind", sa.Enum("DATASET", "NEW_DATASETS", name="kind"), nullable=True,
        ),
    )
    op.alter_column("subscription", "dataset_id", nullable=True)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("subscription", "kind")

    subscription_types = postgresql.ENUM("DATASET", "NEW_DATASETS", name="kind")
    subscription_types.drop(op.get_bind())
    # ### end Alembic commands ###
