"""empty message

Revision ID: 5fdb7eccc5ea
Revises: 98c9e085b1b9
Create Date: 2019-05-23 17:40:31.432820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fdb7eccc5ea'
down_revision = '98c9e085b1b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('account', 'join_date', existing_type=sa.Date(), type_=sa.DateTime())
    op.alter_column('useraccesslog', 'timestamp', existing_type=sa.Date(), type_=sa.DateTime())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('account', 'join_date', existing_type=sa.DateTime(), type_=sa.Date())
    op.alter_column('useraccesslog', 'timestamp', existing_type=sa.DateTime(), type_=sa.Date())
    # ### end Alembic commands ###
