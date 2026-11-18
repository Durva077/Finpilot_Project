"""add optional phone number to users

Revision ID: 3f6372dea81f
Revises: de0ddf4dbc9b
Create Date: 2026-11-18 17:57:30.300306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f6372dea81f'
down_revision: Union[str, Sequence[str], None] = 'de0ddf4dbc9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column('phone_number', sa.String(length=20), nullable=True)
    )
    op.create_unique_constraint(
        'uq_users_phone_number',
        'users',
        ['phone_number']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'uq_users_phone_number',
        'users',
        type_='unique'
    )
    op.drop_column('users', 'phone_number')