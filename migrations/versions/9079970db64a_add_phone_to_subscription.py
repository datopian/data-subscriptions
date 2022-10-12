"""add phone to subscription

Revision ID: 9079970db64a
Revises: cfc89c5e14c7
Create Date: 2022-10-12 16:38:45.897230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9079970db64a'
down_revision = 'cfc89c5e14c7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("subscription", sa.Column(
        "phone_number", sa.Text(), nullable=True))


def downgrade():
    op.drop_column("subscription", "phone_number")
