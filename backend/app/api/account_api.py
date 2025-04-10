from fastapi import APIRouter
from backend.app.dependencies.auth_dep import CurrentUser
from backend.app.dependencies.services import account_service
from backend.app.models.account import AccountRead, AccountReadWithPayments

from backend.core.db import TransactionSessionDep, SessionDep

account_router = APIRouter()


@account_router.post('/account', response_model=AccountRead)
async def create_account(db: TransactionSessionDep, current_user: CurrentUser):
    """
        Создаёт новый счёт для текущего пользователя.

        Если счёт уже существует, новый создан не будет.

        :param db: Асинхронная транзакционная сессия базы данных.
        :param current_user: Текущий авторизованный пользователь.
        :return: Данные созданного счёта.
        """
    return await account_service.create_account(db, current_user)


@account_router.post('/account/{account_id}', response_model=AccountReadWithPayments)
async def get_account_with_transactions(db: SessionDep, account_id: int, current_user: CurrentUser):
    """
        Получает информацию о счёте с указанным ID, включая связанные транзакции.

        Доступ разрешён только владельцу счёта.

        :param db: Асинхронная сессия базы данных.
        :param account_id: Уникальный идентификатор счёта.
        :param current_user: Текущий авторизованный пользователь.
        :return: Данные счёта и его транзакции.
        """
    return await account_service.get_account(db, account_id, current_user)
