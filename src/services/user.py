from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from repository.repository import BaseRepository
from schemas.user import UserCreate, UserDelete, UserUpdate
from utils.error_handling import error_response


async def get_user_info(session: AsyncSession, repository: BaseRepository, email: str | None) -> User:
    filters = {"email": email}

    res = await repository.get_single(User, session, **filters)
    if not res:
        return error_response("Invalid email address.")

    return res


async def get_list_users(
    page: int,
    size: int,
    session: AsyncSession,
    repository: BaseRepository,
) -> dict[str, dict[str, int] | list[User | None]]:
    prev_page = page - 1 if page - 1 > 0 else None
    page = (page - 1) * size

    data = await repository.get(User, session, size, page)

    next_page = page + 1 if data and len(data) == size else None
    result = {
        "links": {
            "prev": prev_page,
            "next": next_page,
        },
        "data": data
    }

    return result


async def update_user_profile(
    data: UserUpdate,
    session: AsyncSession,
    repository: BaseRepository,
) -> User | None:
    filters = {"id": str(data.id)}
    data = data.model_dump()

    res = await repository.update(data, User, session, **filters)
    if not res:
        return error_response("Invalid user ID.")

    return res


async def delete_user_profile(data: UserDelete, session: AsyncSession, repository: BaseRepository) -> dict[str, str]:
    filters = data.model_dump()
    res = await repository.delete(User, session, **filters)
    if not res:
        return error_response("Invalid email address.")

    return res
