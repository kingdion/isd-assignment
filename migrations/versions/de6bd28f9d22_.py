"""empty message

Revision ID: de6bd28f9d22
Revises: 1e3ad7a4c83d
Create Date: 2019-05-31 02:55:22.648995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de6bd28f9d22'
down_revision = '1e3ad7a4c83d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('baddress', sa.String(length=50), nullable=False))
    op.add_column('payment', sa.Column('bfirst', sa.String(length=20), nullable=False))
    op.add_column('payment', sa.Column('blast', sa.String(length=20), nullable=False))
    op.drop_column('payment', 'bfirst_name')
    op.drop_column('payment', 'bstreet_address')
    op.drop_column('payment', 'blast_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('blast_name', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.add_column('payment', sa.Column('bstreet_address', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
    op.add_column('payment', sa.Column('bfirst_name', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.drop_column('payment', 'blast')
    op.drop_column('payment', 'bfirst')
    op.drop_column('payment', 'baddress')
    # ### end Alembic commands ###
