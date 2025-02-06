from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi import APIRouter, Depends, Query
from starlette import status

from models.user import User
from schemas.user import UserDelete, UserInfo, UserUpdate
from services.auth import check_current_user
from services.user import (
    delete_user_profile,
    get_user_info,
    get_list_users,
    update_user_profile,
)
from utils.dependency import db_dependency, repository_dependency
from utils.error_handling import error_response


router = APIRouter(prefix="/api/v1/user", tags=["User"])


@router.get(
    "/info",
    summary="Get user info.",
    status_code=status.HTTP_200_OK,
    response_model=UserInfo,
)
async def get_user(
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT = Depends(),
    email: str | None = None,
):
    current_user = await check_current_user(session, authorize, repository)
    if current_user.is_stuff and email and current_user.email != email:
        user_info = await get_user_info(session, repository, email)

        return user_info

    return current_user


@router.get(
    "/",
    summary="Get list of users.",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, dict[str, int | None] | list[UserInfo | None]]
)
async def get_users(
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT = Depends(),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=50, default=10),
):
    current_user = await check_current_user(session, authorize, repository)
    if not isinstance(current_user, User):
        return current_user

    if not current_user.is_stuff:
        return error_response("Access Denied", status.HTTP_403_FORBIDDEN)

    return await get_list_users(page, size, session, repository)


@router.put(
    "/",
    summary="Update user profile.",
    status_code=status.HTTP_200_OK,
    response_model=UserInfo,
)
async def update_profile(
    user_data: UserUpdate,
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT = Depends(),
):
    current_user = await check_current_user(session, authorize, repository)
    if not isinstance(current_user, User):
        return current_user

    if not current_user.is_stuff:
        return error_response("Access Denied", status.HTTP_403_FORBIDDEN)

    return await update_user_profile(user_data, session, repository)


@router.delete(
    "/",
    summary="Delete user profile.",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
)
async def delete_profile(
    user: UserDelete,
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT = Depends(),
):
    current_user = await check_current_user(session, authorize, repository)
    if not isinstance(current_user, User):
        return current_user

    if not current_user.is_stuff:
        return error_response("Access Denied", status.HTTP_403_FORBIDDEN)

    return await delete_user_profile(user, session, repository)
