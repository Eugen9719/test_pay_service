from fastapi import APIRouter

from backend.app.api.account_api import account_router
from backend.app.api.user_api import user_router
from backend.app.api.webhook import webhook_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(account_router, prefix="/account", tags=["account"])
api_router.include_router(webhook_router, prefix="/webhook", tags=["webhook"])