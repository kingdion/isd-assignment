"""empty message

Revision ID: 46b5d1389e47
Revises: 6e0a8ba1f600
Create Date: 2019-04-17 07:31:45.318697

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '46b5d1389e47'
down_revision = '6e0a8ba1f600'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('moviecopy',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('copy_information', sa.String(length=256), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('sold', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('paymentmethod',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('method_name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('movieorderline',
    sa.Column('copyId', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('orderId', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['copyId'], ['moviecopy.id'], ),
    sa.ForeignKeyConstraint(['orderId'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('copyId', 'orderId')
    )
    op.drop_table('movieorder')
    op.create_unique_constraint(None, 'account', ['id'])
    op.create_unique_constraint(None, 'genre', ['id'])
    op.add_column('orders', sa.Column('methodId', postgresql.UUID(as_uuid=True), nullable=True))
    op.alter_column('orders', 'accountId',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.create_unique_constraint(None, 'orders', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='unique')
    op.alter_column('orders', 'accountId',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.drop_column('orders', 'methodId')
    op.drop_constraint(None, 'genre', type_='unique')
    op.drop_constraint(None, 'account', type_='unique')
    op.create_table('movieorder',
    sa.Column('movieId', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('orderId', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['movieId'], ['movie.id'], name='movieorder_movieId_fkey'),
    sa.ForeignKeyConstraint(['orderId'], ['orders.id'], name='movieorder_orderId_fkey'),
    sa.PrimaryKeyConstraint('movieId', 'orderId', name='movieorder_pkey')
    )
    op.drop_table('movieorderline')
    op.drop_table('paymentmethod')
    op.drop_table('moviecopy')
    # ### end Alembic commands ###
