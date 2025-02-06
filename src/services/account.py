from sqlalchemy.ext.asyncio import AsyncSession

from models.wallet import Account
from repository.repository import BaseRepository


async def get_user_account(
    page: int,
    size: int,
    session: AsyncSession,
    repository: BaseRepository,
    **filters,
) -> list[Account | None]:
    prev_page = page - 1 if page - 1 > 0 else None
    page = (page - 1) * size

    data = await repository.get(Account, session, size, page, **filters)

    next_page = page + 1 if data and len(data) == size else None
    result = {
        "links": {
            "prev": prev_page,
            "next": next_page,
        },
        "data": data,
    }

    return result
