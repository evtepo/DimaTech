from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi import APIRouter, Depends, Query
from starlette import status

from schemas.user import UserCreate, UserDelete, UserInfo, UserUpdate
from services.auth import check_current_user
from services.user import (
    create_user_profile,
    delete_user_profile,
    get_user_info,
    get_list_users,
    update_user_profile,
)
from utils.dependency import db_dependency, repository_dependency
from utils.error_handling import error_response


router = APIRouter(prefix="/api/v1/user", tags=["User"])


@router.get(
    "/{email}",
    summary="Get user info.",
    status_code=status.HTTP_200_OK,
    response_model=UserInfo,
)
async def get_user(
    email: str,
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT = Depends(),
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
    response_model=dict[str, dict[str, int] | list[UserInfo | None]]
)
async def get_users(
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT = Depends(),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=50, default=10),
):
    current_user = await check_current_user(session, authorize, repository)
    if not current_user.is_stuff:
        return error_response("Access Denied", status.HTTP_403_FORBIDDEN)

    return await get_list_users(page, size, session, repository)
    

@router.post(
    "/",
    summary="New user profile.",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInfo,
)
async def create_profile(
    user_data: UserCreate,
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT = Depends(),
):
    await check_current_user(session, authorize, repository)
    
    return await create_user_profile(user_data, session, repository)


@router.put(
    "/{email}",
    summary="Update user profile.",
    status_code=status.HTTP_200_OK,
    response_model=UserInfo,
)
async def update_profile(
    email: str,
    user_data: UserUpdate,
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT,
):
    await check_current_user(session, authorize, repository)

    return await update_user_profile(user_data, email, session, repository)


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
    authorize: AuthJWT,
):
    await check_current_user(session, authorize, repository)

    return await delete_user_profile(user, session, repository)
