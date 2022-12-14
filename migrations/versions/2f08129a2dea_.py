"""empty message

Revision ID: 2f08129a2dea
Revises: 5b82070edeac
Create Date: 2022-12-14 11:21:15.175882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f08129a2dea'
down_revision = '5b82070edeac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservation', sa.Column('workspaceId', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reservation', 'workspaceId')
    # ### end Alembic commands ###
