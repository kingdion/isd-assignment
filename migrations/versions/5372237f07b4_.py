"""empty message

Revision ID: 5372237f07b4
Revises: 611f68cf28b7
Create Date: 2019-05-30 19:00:28.500345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5372237f07b4'
down_revision = '611f68cf28b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dfirst', sa.String(length=20), nullable=False),
    sa.Column('dlast', sa.String(length=20), nullable=False),
    sa.Column('dstreet_address', sa.String(length=50), nullable=False),
    sa.Column('dpostcode', sa.String(length=4), nullable=False),
    sa.Column('cname', sa.String(length=20), nullable=False),
    sa.Column('credit_no', sa.String(length=16), nullable=False),
    sa.Column('cvc', sa.String(length=3), nullable=False),
    sa.Column('month', sa.String(length=2), nullable=False),
    sa.Column('year', sa.String(length=4), nullable=False),
    sa.Column('bfirst_name', sa.String(length=20), nullable=False),
    sa.Column('blast_name', sa.String(length=20), nullable=False),
    sa.Column('bstreet_address', sa.String(length=50), nullable=False),
    sa.Column('bpostcode', sa.String(length=4), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    # ### end Alembic commands ###