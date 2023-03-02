"""empty message

Revision ID: b72fa253647a
Revises: b07f79066097
Create Date: 2023-02-03 20:35:46.486646

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b72fa253647a"
down_revision = "b07f79066097"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "references",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("page", sa.Integer(), nullable=False),
        sa.Column("clue", sa.String(), nullable=False),
        sa.Column("link", sa.String(), nullable=True),
        sa.Column("info", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("references")
