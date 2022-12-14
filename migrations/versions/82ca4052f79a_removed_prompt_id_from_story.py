"""Removed prompt_id from Story

Revision ID: 82ca4052f79a
Revises: b4c51e8218d5
Create Date: 2022-07-25 21:37:47.281262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82ca4052f79a'
down_revision = 'b4c51e8218d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('story', schema=None) as batch_op:
        batch_op.drop_constraint('fk_story_prompt_id_prompt', type_='foreignkey')
        batch_op.drop_column('prompt_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('story', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prompt_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_story_prompt_id_prompt', 'prompt', ['prompt_id'], ['id'])

    # ### end Alembic commands ###
