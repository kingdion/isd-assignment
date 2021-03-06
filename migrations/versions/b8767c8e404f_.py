"""empty message

Revision ID: b8767c8e404f
Revises: bdfb1cbb1917
Create Date: 2019-05-31 22:26:01.322347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8767c8e404f'
down_revision = 'bdfb1cbb1917'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('date_ordered', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'date_ordered')
    # ### end Alembic commands ###
