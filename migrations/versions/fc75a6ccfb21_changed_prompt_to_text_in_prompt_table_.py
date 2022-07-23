"""changed 'prompt' to 'text' in Prompt table, attempt 2

Revision ID: fc75a6ccfb21
Revises: 8fcbf978bb86
Create Date: 2022-05-09 22:37:55.533788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc75a6ccfb21'
down_revision = '8fcbf978bb86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompt', schema=None) as batch_op:
        batch_op.add_column(sa.Column('text', sa.String(), nullable=True))
        batch_op.drop_column('prompt')
        batch_op.alter_column(
                 column_name='prompt',
                 new_column_name='text',
                 existing_type='String',
                 existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prompt', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prompt', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('text')

    # ### end Alembic commands ###
