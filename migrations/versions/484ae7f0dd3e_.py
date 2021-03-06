"""empty message

Revision ID: 484ae7f0dd3e
Revises: 
Create Date: 2019-04-17 07:06:05.203555

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '484ae7f0dd3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('first_name', sa.String(length=25), nullable=False),
    sa.Column('last_name', sa.String(length=25), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=35), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movie',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('releaseDate', sa.Date(), nullable=False),
    sa.Column('thumbnailSrc', sa.String(length=150), nullable=False),
    sa.Column('runtime', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('moviegenre',
    sa.Column('movieId', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('genreId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genreId'], ['genre.id'], ),
    sa.ForeignKeyConstraint(['movieId'], ['movie.id'], ),
    sa.PrimaryKeyConstraint('movieId', 'genreId')
    )
    op.create_table('orders',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('accountId', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('trackingStatus', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['accountId'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movieorder',
    sa.Column('movieId', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('orderId', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['movieId'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['orderId'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('movieId', 'orderId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movieorder')
    op.drop_table('orders')
    op.drop_table('moviegenre')
    op.drop_table('movie')
    op.drop_table('genre')
    op.drop_table('account')
    # ### end Alembic commands ###
