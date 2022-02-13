"""Changing coordinate types

Revision ID: 8344badab728
Revises: b4b1ed4da917
Create Date: 2022-02-14 00:45:27.892614

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8344badab728'
down_revision = 'b4b1ed4da917'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('point', 'lat', type_=sa.Numeric(8, 5))
    op.alter_column('point', 'lon', type_=sa.Numeric(8, 5))


def downgrade():
    op.alter_column('point', 'lat', type_=sa.Float)
    op.alter_column('point', 'lon', type_=sa.Float)
