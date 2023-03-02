"""empty message

Revision ID: b07f79066097
Revises: 
Create Date: 2023-01-11 11:35:07.508826

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b07f79066097"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "page_order",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("page", sa.Integer(), nullable=True),
        sa.Column("order", sa.String(), nullable=True),
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "people",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("role", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "page_refs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("page", sa.Integer(), nullable=True),
        sa.Column("people_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["people_id"],
            ["people.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("page_refs")
    op.drop_table("people")
    op.drop_table("page_order")
