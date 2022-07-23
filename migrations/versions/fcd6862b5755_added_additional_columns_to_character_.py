"""added additional columns to Character table

Revision ID: fcd6862b5755
Revises: 9b3ae048b0e3
Create Date: 2022-05-24 11:16:57.483858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcd6862b5755'
down_revision = '9b3ae048b0e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_column('description')
        batch_op.drop_column('gender')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###