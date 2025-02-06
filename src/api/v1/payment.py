from uuid import UUID

from async_fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi import APIRouter, Depends, Query
from starlette import status

from schemas.payment import PaymentCreate, PaymentInfo
from services.auth import check_current_user
from services.payment import create_new_payment, get_user_payments
from utils.dependency import db_dependency, repository_dependency


router = APIRouter(prefix="/api/v1/payment", tags=["Payment"])


@router.get(
    "/",
    summary="Get payments info.",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, dict[str, int] | list[PaymentInfo | None]],
)
async def get_payments(
    session: db_dependency,
    repository: repository_dependency,
    authorize: AuthJWT = Depends(),
    user_id: UUID |  None = None,
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=10, le=50, default=10),
):
    user = await check_current_user(session, authorize, repository)
    filters = {"user_id": user_id} if user.is_stuff and user_id else {"user_id": user.id}
    
    return await get_user_payments(page, size, session, repository, **filters)


@router.post(
    "/",
    summary="Create payment.",
    status_code=status.HTTP_201_CREATED,
    response_model=PaymentInfo,
)
async def create_payment(
    payment: PaymentCreate,
    session: db_dependency,
    repository: repository_dependency,
):
    return await create_new_payment(payment, session, repository)
