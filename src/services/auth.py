from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from configs.settings import settings
from models.user import User
from repository.repository import BaseRepository
from schemas.user import UserCreate, UserLogIn
from utils.error_handling import error_response


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def check_current_user(session: AsyncSession, authorize: AuthJWT, repository: BaseRepository) -> User:
    try:
        await authorize.jwt_required()
        filters = {"email": await authorize.get_jwt_subject()}
    except Exception:
        return JSONResponse({"msg": "Invalid token."}, status_code=status.HTTP_401_UNAUTHORIZED)

    user = await repository.get_single(User, session, **filters)
    if not user:
        return error_response("Access Denied.", status.HTTP_403_FORBIDDEN)

    return user


async def create_user_profile(
    user: UserCreate,
    session: AsyncSession,
    repository: BaseRepository,
) -> User:
    data = user.model_dump()
    data["password"] = get_password_hash(data["password"])

    new_user = await repository.create(data, User, session)
    if not new_user:
        return error_response("User with this email already exists", status.HTTP_400_BAD_REQUEST)

    return new_user


async def log_in_to_account(
    user: UserLogIn,
    session: AsyncSession,
    authorize: AuthJWT,
    repository: BaseRepository,
) -> dict[str, str]:
    data = user.model_dump()
    del data["password"]
    instance = await repository.get_single(User, session, **data)
    if not instance or not verify_password(user.password, instance.password):
        return error_response("Invalid username or password", status.HTTP_401_UNAUTHORIZED)

    access_token = await authorize.create_access_token(
        subject=instance.email,
        expires_time=settings.access_token_expire_in_seconds,
    )

    await authorize.set_access_cookies(access_token)

    return {"access_token": access_token}
