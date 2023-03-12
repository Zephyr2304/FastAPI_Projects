"""create phone_no

Revision ID: b1e28bdc05a9
Revises: 
Create Date: 2023-03-13 01:50:17.635866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1e28bdc05a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_no',sa.String(),nullable=True))
    pass


def downgrade() -> None:
    pass
