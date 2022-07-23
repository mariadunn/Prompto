"""added 'hints' column to Prompt table

Revision ID: eff7cfe905aa
Revises: 48db6af176d5
Create Date: 2022-07-05 22:03:13.322882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eff7cfe905aa'
down_revision = '48db6af176d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompt', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hints', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompt', schema=None) as batch_op:
        batch_op.drop_column('hints')

    # ### end Alembic commands ###
