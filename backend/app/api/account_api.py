from fastapi import APIRouter
from backend.app.dependencies.auth_dep import CurrentUser
from backend.app.dependencies.services import account_service
from backend.app.models.account import AccountRead, AccountReadWithPayments

from backend.core.db import TransactionSessionDep, SessionDep

account_router = APIRouter()


@account_router.post('/account', response_model=AccountRead)
async def create_account(db: TransactionSessionDep, current_user: CurrentUser):
    return await account_service.create_account(db, current_user)


@account_router.post('/account/{account_id}', response_model=AccountReadWithPayments)
async def get_account_with_transactions(db: SessionDep, account_id: int, current_user: CurrentUser):
    return await account_service.get_account(db, account_id, current_user)
