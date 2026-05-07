"""add avatar_url to users

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-08
"""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("avatar_url", sa.String(1024), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "avatar_url")
