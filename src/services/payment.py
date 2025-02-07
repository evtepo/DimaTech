import hashlib

from sqlalchemy.ext.asyncio import AsyncSession

from configs.settings import settings
from models.wallet import Account, Payment
from repository.repository import BaseRepository
from schemas.payment import PaymentCreate
from utils.error_handling import error_response


async def get_user_payments(
    page: int,
    size: int,
    session: AsyncSession,
    repository: BaseRepository,
    **filters
) -> dict[str, dict[str, int] | list[Payment | None]]:
    prev_page = page - 1 if page - 1 > 0 else None
    page = (page - 1) * size

    data = await repository.get(Payment, session, size, page, **filters)

    next_page = page + 1 if data and len(data) == size else None
    result = {
        "links": {
            "prev": prev_page,
            "next": next_page,
        },
        "data": data
    }

    return result


async def create_new_payment(data: PaymentCreate, session: AsyncSession, repository: BaseRepository) -> Payment:
    data_string = f"{data.account_id}{data.amount}{data.transaction_id}{data.user_id}{settings.signature_secret_key}"
    signature = hashlib.sha256(data_string.encode()).hexdigest()
    if signature != data.signature:
        return error_response("Invalid signature.")

    check_transaction = await repository.get_single(Payment, session, transaction_id=data.transaction_id)

    if check_transaction:
        return error_response("The operation has already been completed.")

    account = await repository.get_single(Account, session, id=data.account_id)
    if not account:
        account_data = {"id": data.account_id, "user_id": data.user_id, "balance": 0.0}
        account = await repository.create(account_data, Account, session)
        if not account:
            return error_response("Something went wrong.")

    account.balance = float(account.balance) + data.amount

    data = data.model_dump()
    del data["signature"]

    return await repository.create(data, Payment, session)
