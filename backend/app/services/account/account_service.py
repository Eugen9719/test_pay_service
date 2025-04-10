import uuid
from decimal import Decimal
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.app.models import User
from backend.app.models.account import Account
from backend.app.repositories.account_repositories import AccountRepository
from backend.app.services.auth.permission import PermissionService


class AccountService:
    def __init__(self, account_repository: AccountRepository, permissions: PermissionService):
        """
        Сервис для управления счетами пользователей.

        :param account_repository: Репозиторий для работы с моделью Account.
        :param permissions: Сервис для проверки прав доступа.
        """
        self.account_repository = account_repository
        self.permissions = permissions

    async def create_account(self, db: AsyncSession, current_user: User) -> Account:
        """
        Создаёт новый счёт для указанного пользователя.

        :param db: Асинхронная транзакционная сессия базы данных.
        :param current_user: Пользователь, для которого создаётся счёт.
        :return: Объект созданного счёта.
        """
        account_number = f"ACC-{uuid.uuid4().hex[:8].upper()}"  # Пример: "ACC-A1B2C3D4"

        account = Account(
            account_number=account_number,
            user_id=current_user.id,
            balance=Decimal('0.00')  # Начальный баланс
        )

        account = await self.account_repository.save_db(db, account)
        return account

    async def get_account(self, db: AsyncSession, account_id: int, current_user: User):
        """
        Получает информацию о счёте с транзакциями, если пользователь является владельцем.

        :param db: Асинхронная сессия базы данных.
        :param account_id: ID счёта.
        :param current_user: Текущий пользователь, для проверки прав доступа.
        :return: Объект счёта с транзакциями.
        :raises HTTPException: Если пользователь не владелец счёта.
        """
        account = await self.account_repository.get_or_404(
            db, id=account_id, options=[selectinload(Account.payments)]
        )
        self.permissions.verify_owner_account(account, current_user)
        return account
