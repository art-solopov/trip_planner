"""Create trips

Revision ID: da9e6155c3d6
Revises: f5ca23d0e53b
Create Date: 2020-01-07 01:06:40.734879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da9e6155c3d6'
down_revision = 'f5ca23d0e53b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trip',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=2000), nullable=False),
    sa.Column('country_code', sa.String(length=2), nullable=True),
    sa.Column('slug', sa.String(length=2000), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_trip_author_slug', 'trip', ['author_id', 'slug'], unique=True)
    op.create_index(op.f('ix_trip_author_id'), 'trip', ['author_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_trip_author_id'), table_name='trip')
    op.drop_index('idx_trip_author_slug', table_name='trip')
    op.drop_table('trip')
    # ### end Alembic commands ###