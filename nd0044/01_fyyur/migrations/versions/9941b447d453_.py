"""empty message

Revision ID: 9941b447d453
Revises: cb13d9a58481
Create Date: 2022-05-25 14:19:40.300873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9941b447d453'
down_revision = 'cb13d9a58481'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('website', sa.String(length=512), nullable=True))
    op.add_column('artists', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('artists', sa.Column('seeking_description', sa.String(), nullable=True))
    op.add_column('venues', sa.Column('genres', sa.String(length=256), nullable=True))
    op.add_column('venues', sa.Column('website', sa.String(length=512), nullable=True))
    op.add_column('venues', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('venues', sa.Column('seeking_description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venues', 'seeking_description')
    op.drop_column('venues', 'seeking_talent')
    op.drop_column('venues', 'website')
    op.drop_column('venues', 'genres')
    op.drop_column('artists', 'seeking_description')
    op.drop_column('artists', 'seeking_venue')
    op.drop_column('artists', 'website')
    # ### end Alembic commands ###
