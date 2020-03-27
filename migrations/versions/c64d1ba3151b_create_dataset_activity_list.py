"""create_dataset_activity_list

Revision ID: c64d1ba3151b
Revises: 9e3e665c6a2e
Create Date: 2020-03-24 14:01:57.185283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c64d1ba3151b"
down_revision = "9e3e665c6a2e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "dataset_activity_list",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("blob", sa.JSON()),
        sa.Column("last_activity_created_at", sa.DateTime(), nullable=True),
        sa.Column("collected_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("dataset_activity_list")
