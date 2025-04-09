from fastapi import FastAPI
from backend.app import routers
from backend.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    DEBUG=True
)

app.include_router(routers.api_router, prefix=settings.API_V1_STR)
