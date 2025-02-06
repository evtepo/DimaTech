from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi import APIRouter, Depends
from starlette import status

from models.user import User
from schemas.auth import TokenSettings
from schemas.user import UserCreate, UserInfo, UserLogIn
from services.auth import check_current_user, create_user_profile, log_in_to_account
from utils.dependency import db_dependency, repository_dependency
from utils.error_handling import error_response


router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@AuthJWT.load_config
def get_config():
    return TokenSettings()


@router.post(
    "/register",
    summary="Sign up a new user.",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInfo,
)
async def create_user(
    user: UserCreate,
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT = Depends(),
):
    current_user = await check_current_user(session, authorize, repository)
    if not isinstance(current_user, User):
        return current_user

    if not current_user.is_stuff:
        return error_response("Access Denied.", status.HTTP_403_FORBIDDEN)

    return await create_user_profile(user, session, repository)


@router.post(
    "/login",
    summary="Log in to account.",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
)
async def login(
    user: UserLogIn,
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT = Depends(),
):
    return await log_in_to_account(user, session, authorize, repository)


@router.delete(
    "/logout",
    summary="Log out of account.",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
)
async def logout(authorize: AuthJWT = Depends()):
    await authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}
