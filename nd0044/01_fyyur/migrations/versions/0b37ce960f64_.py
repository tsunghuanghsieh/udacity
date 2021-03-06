"""empty message

Revision ID: 0b37ce960f64
Revises: 9941b447d453
Create Date: 2022-05-28 16:07:43.513688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b37ce960f64'
down_revision = '9941b447d453'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    SHOWS_ID_SEQ = sa.Sequence('shows_id_seq')
    op.execute(sa.schema.CreateSequence(SHOWS_ID_SEQ))
    op.create_table('shows',
    sa.Column('id', sa.Integer(), SHOWS_ID_SEQ, server_default = SHOWS_ID_SEQ.next_value(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'artist_id', 'venue_id')
   )
    op.execute('ALTER SEQUENCE shows_id_seq OWNED BY shows.id;')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shows')
    # ### end Alembic commands ###
