"""empty message

Revision ID: bdfb1cbb1917
Revises: 5a2915ca266e
Create Date: 2019-05-31 21:32:46.182844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdfb1cbb1917'
down_revision = '5a2915ca266e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('join_date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payment', 'join_date')
    # ### end Alembic commands ###
