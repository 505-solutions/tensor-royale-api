"""build migration

Revision ID: 5333e9b33e32
Revises: 934accbfe85a
Create Date: 2024-03-16 13:11:27.072745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5333e9b33e32'
down_revision = '934accbfe85a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('problem')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('problem',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('timestamp', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('deadline', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('reward', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('solved', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('submissions_count', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='problem_pkey')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('wallet', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    # ### end Alembic commands ###