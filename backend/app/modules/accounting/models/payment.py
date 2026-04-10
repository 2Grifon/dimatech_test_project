from decimal import Decimal
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_models import Base, UUIDMixin, CreatedAtMixin

if TYPE_CHECKING:
    from app.modules.accounting.models import Account


class Payment(UUIDMixin, CreatedAtMixin, Base):
    __tablename__ = "payment"

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        unique=True,
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=18, scale=2),
        nullable=False,
    )

    account: Mapped["Account"] = relationship(back_populates="payments")
