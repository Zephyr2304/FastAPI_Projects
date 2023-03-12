"""Create address_id to users

Revision ID: 85d139cee8eb
Revises: 28de43df3dee
Create Date: 2023-03-13 02:20:07.335947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d139cee8eb'
down_revision = 'dcceab6fb058'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users',sa.Column('address_id',sa.Integer(),nullable=True))
    op.create_foreign_key('address_user_fk',source_table='users',referent_table='address',
                          local_cols=['address_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('address_user_fk',table_name='users')
    op.drop_column('users','address_id')
    pass
