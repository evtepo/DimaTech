from uuid import UUID

from pydantic import BaseModel


class AccountMixin(BaseModel):
    balance: float
    user_id: UUID


class AccountInfo(AccountMixin):
    id: UUID
