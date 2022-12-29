"""Initial migration.

Revision ID: 0722b52013df
Revises: 
Create Date: 2022-12-29 20:04:30.585286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0722b52013df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('people',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('page', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('page', sa.Integer(), nullable=True),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('people')
    op.drop_table('pages')
