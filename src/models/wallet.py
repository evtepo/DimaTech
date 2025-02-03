import uuid

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db_connect import Base
from models.base import BaseModel


class Account(Base, BaseModel):
    balance: Mapped[float] = mapped_column(Numeric(11, 2), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("user.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="accounts")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="account")


class Payment(Base, BaseModel):
    transaction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(11, 2), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("user.id"),
        nullable=False,
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("account.id"),
        nullable=False,
    )

    account: Mapped["Account"] = relationship("Account", back_populates="payments")
