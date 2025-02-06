from uuid import UUID

from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi import APIRouter, Depends, Query
from starlette import status

from models.user import User
from schemas.account import AccountInfo
from services.account import get_user_account
from services.auth import check_current_user
from utils.dependency import db_dependency, repository_dependency


router = APIRouter(prefix="/api/v1/account", tags=["Account"])


@router.get(
    "/",
    summary="Get user account information.",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, dict[str, int | None] | list[AccountInfo | None]],
)
async def get_account(
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT = Depends(),
    user_id: UUID | None = None,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=50, default=10),
):
    user = await check_current_user(session, authorize, repository)
    if not isinstance(user, User):
        return user

    filters = {"user_id": user_id} if user.is_stuff and user_id else {"user_id": user.id}

    return await get_user_account(page, size, session, repository, **filters)
