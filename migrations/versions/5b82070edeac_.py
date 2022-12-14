"""empty message

Revision ID: 5b82070edeac
Revises: ff521e2442bb
Create Date: 2022-12-07 18:18:04.031309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b82070edeac'
down_revision = 'ff521e2442bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Integer(), nullable=True),
    sa.Column('start', sa.Integer(), nullable=True),
    sa.Column('end', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('workspace_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('workspace', 'model',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('workspace', 'model',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.drop_table('reservation')
    # ### end Alembic commands ###
