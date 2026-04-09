from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import String, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_models import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.modules.accounting.models import Account


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # is_active: Mapped[bool] = mapped_column(default=True, nullable=False) # Сделать "мягкое"
    #  удаление?
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="userrole"),
        default=UserRole.user,
        nullable=False,
    )

    accounts: Mapped[list["Account"]] = relationship(back_populates="user")
