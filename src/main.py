import uvicorn
from fastapi import FastAPI

from api.v1.account import router as account_router
from api.v1.auth import router as auth_router
from api.v1.user import router as user_router
from api.v1.payment import router as payment_router
from configs.settings import settings


app = FastAPI(
    title=settings.service_name,
    version="1.0"
)

app.include_router(account_router)
app.include_router(auth_router)
app.include_router(payment_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.service_host,
        port=settings.service_port,
    )
