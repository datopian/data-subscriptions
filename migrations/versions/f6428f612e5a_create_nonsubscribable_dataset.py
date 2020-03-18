"""create_nonsubscribable_dataset

Revision ID: f6428f612e5a
Revises: 3c403aee5d08
Create Date: 2020-03-18 08:50:54.004440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f6428f612e5a"
down_revision = "3c403aee5d08"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "nonsubscribable_dataset",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("dataset_id", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("dataset_id"),
    )


def downgrade():
    op.drop_table("nonsubscribable_dataset")
