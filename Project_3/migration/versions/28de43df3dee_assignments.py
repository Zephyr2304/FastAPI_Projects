"""Assignments

Revision ID: 28de43df3dee
Revises: b1e28bdc05a9
Create Date: 2023-03-13 02:03:44.576450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28de43df3dee'
down_revision = '85d139cee8eb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address',sa.Column('apt_num',sa.String(),nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('address','apt_num')
    pass
