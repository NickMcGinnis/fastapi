"""add fk to post tabl

Revision ID: a6c3168f3c01
Revises: c02f7da93696
Create Date: 2024-08-21 22:43:00.353985

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a6c3168f3c01"
down_revision: Union[str, None] = "c02f7da93696"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    op.create_foreign_key(
        "post_users_fk", "posts", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("post_users_fk", "posts", type_="foreignkey")
    op.drop_column("posts", "user_id")
