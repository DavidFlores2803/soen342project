"""empty message

Revision ID: ab380d054092
Revises: 
Create Date: 2024-11-12 16:17:11.673147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab380d054092'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('offerings', schema=None) as batch_op:
        batch_op.alter_column('shedule_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('offerings', schema=None) as batch_op:
        batch_op.alter_column('shedule_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
