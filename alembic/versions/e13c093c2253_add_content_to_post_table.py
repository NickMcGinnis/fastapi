"""add content to post table

Revision ID: e13c093c2253
Revises: 90175c97c306
Create Date: 2024-08-21 22:31:02.769074

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e13c093c2253"
down_revision: Union[str, None] = "90175c97c306"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
