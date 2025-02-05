from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi import APIRouter, Depends
from starlette import status

from schemas.user import UserCreate, UserDelete, UserInfo, UserUpdate
from services.auth import check_current_user
from services.user import (
    create_user_profile,
    delete_user_profile,
    get_user_info,
    update_user_profile,
)
from utils.dependency import db_dependency, repository_dependency


router = APIRouter(prefix="/api/v1/user", tags=["User"])


@router.get(
    "/",
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
    if current_user.is_stuff and email:
        user_info = await get_user_info(session, repository, email)

        return user_info

    return current_user


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
