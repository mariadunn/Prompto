"""added Universe table

Revision ID: e4bdef23b10f
Revises: 50ebf8238fbe
Create Date: 2022-03-31 11:13:20.048536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4bdef23b10f'
down_revision = '50ebf8238fbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('universe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('universe', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_universe_name'), ['name'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('universe', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_universe_name'))

    op.drop_table('universe')
    # ### end Alembic commands ###
