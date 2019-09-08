"""initial

Revision ID: 97a7b54f7a9e
Revises: 
Create Date: 2019-09-08 23:24:47.199935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97a7b54f7a9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.String(32), nullable=False),
    sa.Column('display_name', sa.String(32), nullable=False),
    sa.Column('password', sa.String(64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    raise Exception()
    op.drop_table('accounts')
    # ### end Alembic commands ###