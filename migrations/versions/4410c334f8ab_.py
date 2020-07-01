"""empty message

Revision ID: 4410c334f8ab
Revises: bff937d0113d
Create Date: 2020-05-05 23:32:46.585632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4410c334f8ab'
down_revision = 'bff937d0113d'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('point', 'schedule', new_column_name='schedule_old')


def downgrade():
    op.alter_column('point', 'schedule_old', new_column_name='schedule')
