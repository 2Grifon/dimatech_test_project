"""Seed user, admin and account

Revision ID: 27093299c4d3
Revises: e2f418f376f4
Create Date: 2026-04-10 15:26:40.306781

Default credentials

User:  user@example.com  / userpassword123
Admin: admin@example.com / adminpassword123

"""

from datetime import datetime, timezone
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher


# revision identifiers, used by Alembic.
revision: str = "27093299c4d3"
down_revision: Union[str, Sequence[str], None] = "e2f418f376f4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

password_hash = PasswordHash((Argon2Hasher(), BcryptHasher()))


def now() -> datetime:
    return datetime.now(timezone.utc)


USER_ID = uuid.uuid4()
ADMIN_ID = uuid.uuid4()
ACCOUNT_ID = uuid.uuid4()


def upgrade() -> None:
    """Upgrade schema."""
    ts = now()

    bind = op.get_bind()
    meta = sa.MetaData()
    meta.reflect(bind=bind)

    user_table = meta.tables["user"]
    account_table = meta.tables["account"]

    op.bulk_insert(
        user_table,
        [
            {
                "id": USER_ID,
                "email": "user@example.com",
                "hashed_password": password_hash.hash("userpassword123"),
                "full_name": "Test User",
                "is_active": True,
                "role": "user",
                "created_at": ts,
                "updated_at": ts,
            },
            {
                "id": ADMIN_ID,
                "email": "admin@example.com",
                "hashed_password": password_hash.hash("adminpassword123"),
                "full_name": "Test Admin",
                "is_active": True,
                "role": "admin",
                "created_at": ts,
                "updated_at": ts,
            },
        ],
    )

    op.bulk_insert(
        account_table,
        [
            {
                "id": ACCOUNT_ID,
                "user_id": USER_ID,
                "balance": "0.00",
                "created_at": ts,
                "updated_at": ts,
            },
        ],
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
