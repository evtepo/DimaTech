import uvicorn
from fastapi import FastAPI

from api.v1.auth import router as auth_router
from api.v1.user import router as user_router
from configs.settings import settings


app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.service_host,
        port=settings.service_port,
        reload=True,
    )
