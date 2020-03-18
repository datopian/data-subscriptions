"""create_nonsubscribable_dataset

Revision ID: 1247113bbe45
Revises: 3c403aee5d08
Create Date: 2020-03-18 09:53:23.051850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1247113bbe45"
down_revision = "3c403aee5d08"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "nonsubscribable_dataset",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("dataset_id", sa.Text(), nullable=False, unique=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("nonsubscribable_dataset")
