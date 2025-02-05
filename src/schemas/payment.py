from uuid import UUID

from pydantic import BaseModel


class PaymentMixin(BaseModel):
    transaction_id: UUID
    amount: float
    user_id: UUID
    account_id: UUID


class PaymentInfo(PaymentMixin):
    id: UUID


class PaymentCreate(PaymentMixin):
    signature: str
