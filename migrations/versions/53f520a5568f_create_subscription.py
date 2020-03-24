"""create_subscription

Revision ID: 53f520a5568f
Revises: 6356cd229013
Create Date: 2020-03-24 09:57:41.958418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "53f520a5568f"
down_revision = "6356cd229013"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "subscription",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("dataset_id", sa.Text(), nullable=False),
        sa.Column("user_id", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("dataset_id"),
        sa.UniqueConstraint("user_id"),
    )


def downgrade():
    op.drop_table("subscription")
