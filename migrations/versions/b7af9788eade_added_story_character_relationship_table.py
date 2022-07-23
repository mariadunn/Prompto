"""added story_character relationship table

Revision ID: b7af9788eade
Revises: b1eceb341663
Create Date: 2022-04-06 10:55:01.472060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7af9788eade'
down_revision = 'b1eceb341663'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('story_character',
    sa.Column('story_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['story_id'], ['story.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('story_character')
    # ### end Alembic commands ###
