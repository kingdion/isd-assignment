"""empty message

Revision ID: e253515c9517
Revises: 46b5d1389e47
Create Date: 2019-04-18 20:11:01.728996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e253515c9517'
down_revision = '46b5d1389e47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('is_staff', sa.Boolean(), nullable=False))
    op.add_column('account', sa.Column('postcode', sa.Integer(), nullable=False))
    op.add_column('account', sa.Column('street_address', sa.String(length=100), nullable=False))
    op.drop_column('movie', 'is_staff')
    op.drop_column('movie', 'street_address')
    op.drop_column('movie', 'postcode')
    op.create_unique_constraint(None, 'moviecopy', ['id'])
    op.create_unique_constraint(None, 'paymentmethod', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'paymentmethod', type_='unique')
    op.drop_constraint(None, 'moviecopy', type_='unique')
    op.add_column('movie', sa.Column('postcode', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('movie', sa.Column('street_address', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.add_column('movie', sa.Column('is_staff', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('account', 'street_address')
    op.drop_column('account', 'postcode')
    op.drop_column('account', 'is_staff')
    # ### end Alembic commands ###
