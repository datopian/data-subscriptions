"""add_standard_attributes_to_all_models

Revision ID: 89316d8bd746
Revises: c64d1ba3151b
Create Date: 2020-03-26 17:26:33.570950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "89316d8bd746"
down_revision = "c64d1ba3151b"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "nonsubscribable_dataset",
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.add_column(
        "nonsubscribable_dataset",
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.add_column(
        "subscription", sa.Column("created_at", sa.DateTime(), nullable=False)
    )
    op.add_column(
        "subscription", sa.Column("updated_at", sa.DateTime(), nullable=False)
    )


def downgrade():
    op.drop_column("subscription", "updated_at")
    op.drop_column("subscription", "created_at")
    op.drop_column("nonsubscribable_dataset", "updated_at")
    op.drop_column("nonsubscribable_dataset", "created_at")
